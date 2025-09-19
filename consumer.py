#!/usr/bin/env python3
"""
Task Consumer Runner
Runs the task consumer independently from the API server
"""
import asyncio
import logging
from application.config.app_config import AppConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting standalone task consumer...")

    app_config = AppConfig()

    try:
        # Start the task consumer
        await app_config.task_consumer_config.start_consumer()
    except KeyboardInterrupt:
        logger.info("Shutting down task consumer...")
        await app_config.task_consumer_config.stop_consumer()
        logger.info("Task consumer stopped")
    except Exception as e:
        logger.error(f"Error in task consumer: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())