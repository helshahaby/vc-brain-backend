# main.py
import os
from dotenv import load_dotenv

load_dotenv() # This automatically injects the .env file values into os.environ

import asyncio
import logging

from uuid import UUID, uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from supabase import create_client

from agent_engine import DebateResult, execute_vc_debate


logger = logging.getLogger(__name__)
app = FastAPI()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


class StartupPayload(BaseModel):
    startup_id: UUID
    linkedin: HttpUrl | None = None
    github: HttpUrl | None = None


@app.post("/api/analyze", status_code=202)
async def analyze_startup(payload: StartupPayload, background_tasks: BackgroundTasks):
    run_id = str(uuid4())

    # Atomic claim: only one currently eligible request can start analysis.
    claim = (
        supabase.table("startups")
        .update({
            "status": "queued",
            "analysis_run_id": run_id,
            "decision": None,
            "confidence_score": None,
            "founder_trust": None,
            "tech_trust": None,
        })
        .eq("id", str(payload.startup_id))
        .in_("status", ["new", "failed"])
        .select("id, name")
        .execute()
    )

    if not claim.data:
        raise HTTPException(
            status_code=409,
            detail="Startup does not exist or is already being analyzed.",
        )

    startup = claim.data[0]
    background_tasks.add_task(
        run_agent_pipeline,
        startup["id"],
        startup["name"],
        str(payload.linkedin) if payload.linkedin else None,
        str(payload.github) if payload.github else None,
        run_id,
    )
    return {"status": "queued", "startup_id": startup["id"], "run_id": run_id}


async def run_agent_pipeline(
    startup_id: str,
    name: str,
    linkedin: str | None,
    github: str | None,
    run_id: str,
) -> None:
    try:
        # Avoid blocking the event loop if using the synchronous Supabase client.
        await asyncio.to_thread(
            lambda: (
                supabase.table("startups")
                .update({"status": "running"})
                .eq("id", startup_id)
                .eq("analysis_run_id", run_id)
                .execute()
            )
        )

        result = await execute_vc_debate(name, linkedin, github)

        response = await asyncio.to_thread(
            lambda: (
                supabase.table("startups")
                .update({
                    **result.model_dump(),
                    "status": "completed",
                })
                .eq("id", startup_id)
                .eq("analysis_run_id", run_id)
                .select("id, status")
                .execute()
            )
        )

        if not response.data:
            logger.warning("Skipped stale completion for startup=%s run=%s", startup_id, run_id)

    except Exception:
        logger.exception("Analysis failed for startup=%s run=%s", startup_id, run_id)

        # Cannot overwrite a newer run.
        await asyncio.to_thread(
            lambda: (
                supabase.table("startups")
                .update({"status": "failed"})
                .eq("id", startup_id)
                .eq("analysis_run_id", run_id)
                .execute()
            )
        )