import datetime

def start_session(fuzzer, courier, oracles, logger, n_test_cases):
    logger.write("# Session started at " + str(datetime.datetime.now()))

    for i in range(1, n_test_cases+1):
        logger.write("# Test Case no. " + str(i))
        fuzz_data, fuzz_metadata = fuzzer.fuzz()
        deliver_retval = courier.deliver(fuzz_data)

        logger.write("fuzz_data:")
        logger.write(fuzz_data)
        logger.write("fuzz_metadata:")
        logger.write(fuzz_metadata)
        logger.write("deliver_retval:")
        logger.write(deliver_retval)

        for oracle in oracles:
            logger.write(oracle.report())

    logger.write("# Session ended at " + str(datetime.datetime.now()))

    return 0
