"""Log a parse-run summary."""

from __future__ import annotations

from loguru import logger

from cs_medal_parser.images.result import ProcessingResult


def log_summary(results: list[ProcessingResult], elapsed_seconds: float) -> None:
    succeeded = sum(1 for result in results if result.success)
    failed = len(results) - succeeded

    logger.info("Processing Summary:")
    logger.info("  • Total images processed: {}", len(results))
    logger.info("  • Successful: {}", succeeded)
    logger.info("  • Failed: {}", failed)
    logger.info("  • Execution time: {:.2f} seconds", elapsed_seconds)

    if failed:
        logger.warning("Failed to process {} images", failed)
        for result in [item for item in results if not item.success][:5]:
            logger.debug("Failed: {} - {}", result.image_name, result.error_message)

    logger.success("CS medal parser completed in {:.2f} seconds", elapsed_seconds)
