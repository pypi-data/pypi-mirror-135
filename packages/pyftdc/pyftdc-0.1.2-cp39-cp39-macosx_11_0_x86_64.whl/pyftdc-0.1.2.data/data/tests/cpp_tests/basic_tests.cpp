//
// Created by jorge on 12/25/20.
//

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN  // in only one cpp file

#define BOOST_TEST_MODULE ftdc_basic_suite

#include <boost/test/unit_test.hpp>
#include <boost/format.hpp>

#include <fstream>
#include <FTDCParser.h>
#include <Chunk.h>
#include <iostream>
#include <boost/thread.hpp>

#include <filesystem>

// Run in the test directory
static const char *DATA_TEST_FILE_NAME = "./cpp_tests/metrics.data";
static const char *CSV__TEST_FILE_NAME = "./cpp_tests/first.csv";
static const char *DATA_TEST_DIR = "./diagnostic.data_40/";


int ParserTaskConsumerThread(ParserTasksList *parserTasks, Dataset *dataSet);

static
std::vector<ChunkMetric *>
readMetricsFromCSV() {

    std::vector<ChunkMetric *> metrics;
    metrics.reserve(1500);

    //
    std::ifstream f;
    f.open(CSV__TEST_FILE_NAME, std::ios::in);
    std::string line;
    while (getline(f, line)) { //read data from file object and put it into string.

        std::stringstream ss(line);
        std::string token;
        ChunkMetric *pM = nullptr;
        int field = 0;
        do {
            std::getline(ss, token, ':');

            if (!pM) {
                pM = new ChunkMetric(token, BSON_TYPE_INT64, 0);
            } else {
                pM->values[field++] = atol(token.c_str());
            }

        } while (field < 300);
        metrics.emplace_back(pM);
    }
    f.close();

    return metrics;
}


BOOST_AUTO_TEST_SUITE(ftdc_basic_suite)


    BOOST_AUTO_TEST_CASE(OpenFile) {

        // Create parser
        auto *parser = new FTDCParser();

        auto file_path = std::filesystem::current_path();
        file_path.append(DATA_TEST_FILE_NAME);
        BOOST_TEST_MESSAGE(file_path);

        auto reader = parser->open(file_path);
        BOOST_CHECK_NE(reader, nullptr);

        bson_reader_destroy(reader);

        delete parser;
    }

    BOOST_AUTO_TEST_CASE(ReadInfoChunk) {

        // Create parser
        auto *parser = new FTDCParser();

        auto file_path = std::filesystem::current_path();
        file_path.append(DATA_TEST_FILE_NAME);
        BOOST_TEST_MESSAGE(file_path);
        auto reader = parser->open(file_path);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        bson_reader_destroy(reader);
        delete parser;
        BOOST_CHECK_EQUAL(1, 1);
    }

    BOOST_AUTO_TEST_CASE(ReadDataChunk) {

        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break; // <-- only one!

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);
        BOOST_CHECK(pChunk);

        bson_reader_destroy(reader);

        delete parser;
        BOOST_CHECK_EQUAL(1, 1);
    }

    BOOST_AUTO_TEST_CASE(checkMetricNames) {

        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);

        parser->parseInfoChunk(pBsonChunk);

        // - - - - - - - - - -
        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break;

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);

        BOOST_CHECK(pChunk);

        auto decomp_result = pChunk->Decompress();
        auto data = pChunk->getUncompressedData();
        BOOST_CHECK(data);
        auto dataSize = pChunk->getUncompressedSize();
        BOOST_CHECK(dataSize);

        // We construct the metrics. This are name and first value only since deltas have not been read.
        int metrics = pChunk->ConstructMetrics(data);
        BOOST_CHECK_EQUAL(metrics, pChunk->getMetricsCount());

        // Get names
        std::vector<std::string> metricsNames;
        pChunk->getMetricNames(metricsNames);

        // Compare first 1000 names
        for (int m = 0; m < 1000; ++m) {

            auto pMetric = pChunk->getMetric(m);
            BOOST_CHECK(pMetric);

            BOOST_CHECK_EQUAL(pMetric->name, metricsNames[m]);
        }

        //
        bson_reader_destroy(reader);

        delete parser;
    }


    BOOST_AUTO_TEST_CASE(compareMetrics_1) {
        // Create parser
        auto parser = new FTDCParser();

        auto reader = parser->open(DATA_TEST_FILE_NAME);
        BOOST_CHECK(reader);

        auto pBsonChunk = bson_reader_read(reader, 0);


        parser->parseInfoChunk(pBsonChunk);

        // - - - - - - - - - -
        pBsonChunk = bson_reader_read(reader, 0);

        Dataset dataset;
        ParserTasksList parserTasks;
        int64_t id;
        bson_iter_t iter;
        if (bson_iter_init(&iter, pBsonChunk)) {
            while (bson_iter_next(&iter)) {

                if (BSON_ITER_HOLDS_BINARY(&iter)) {
                    bson_subtype_t subtype;
                    uint32_t bin_size;
                    const uint8_t *data;
                    bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                    // the memory pointed to by data is managed internally. Better make a copy
                    uint8_t *bin_data = new uint8_t[bin_size];
                    memcpy(bin_data, data, bin_size);
                    parserTasks.push(bin_data, bin_size, id);

                    break;

                } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {
                    id = bson_iter_date_time(&iter);
                }
            }
        }

        size_t numThreads = boost::thread::hardware_concurrency();
        boost::thread_group threads;
        for (size_t i = 0; i < numThreads; ++i)
            threads.add_thread(new boost::thread(ParserTaskConsumerThread, &parserTasks, &dataset));

        // Wait for threads to finish
        threads.join_all();

        BOOST_CHECK_EQUAL(dataset.getChunkCount(), 1);

        auto pChunk = dataset.getChunk(0);
        BOOST_CHECK(pChunk);

        auto data = pChunk->getUncompressedData();
        BOOST_CHECK(data);
        auto dataSize = pChunk->getUncompressedSize();
        BOOST_CHECK(dataSize);

        // We construct the metrics. These are name and first value only since deltas have not been read.
        int metrics = pChunk->ConstructMetrics(data);
        BOOST_CHECK_EQUAL(metrics, pChunk->getMetricsCount());

        auto readMetrics = readMetricsFromCSV();
        // Get names
        pChunk->ReadVariableSizedInts();

        int brokenMetrics = 0;
        for (int i = 0; i < readMetrics.size(); ++i) {
            auto pMetric = pChunk->getMetric(i);
            auto pMetricsFromCSV = readMetrics[i];

            // compare
            BOOST_TEST_MESSAGE(pMetric->name);

            for (int j = 0; j < 300; ++j) {

                if (pMetric->values[j] != pMetricsFromCSV->values[j]) {

                    uint64_t diff = pMetric->values[j] - pMetricsFromCSV->values[j];

                    auto errs = str(
                            boost::format("ChunkMetric %1% %2% diverges index %3%  abs(%4%)  Is %5%  should be %6%")
                            % pMetric->name.c_str() % i % j % std::abs((long) (diff)) % pMetric->values[j] %
                            pMetricsFromCSV->values[j]);

                    ++brokenMetrics;
                    BOOST_TEST_MESSAGE(errs);
                    break;
                }
            }
        }

        BOOST_CHECK_EQUAL(brokenMetrics, 0);
        //
        bson_reader_destroy(reader);
    }


    BOOST_AUTO_TEST_CASE(timestamp_dataset_monotony) {     // Are timestamps sequential?
        // Create parser
        auto parser = new FTDCParser();

        //parser->keepChunkStructures(true);  // Do not release Chunks after parsing is done.

        std::vector<std::string> files;

        files.emplace_back(DATA_TEST_FILE_NAME);

        auto status = parser->parseFiles(&files, false, false);

        BOOST_CHECK_EQUAL(status, 0);
        auto chunkVector = parser->getChunks();

        BOOST_CHECK_GT(chunkVector.size(), 1);

        for (int i = 1; i < chunkVector.size(); ++i) {
            auto prevChunkFinalTimestamp = chunkVector[i - 1]->getEnd() / 1000;
            auto thisChunkInitialTimestamp = chunkVector[i]->getStart() / 1000;

            if (prevChunkFinalTimestamp + 1 != thisChunkInitialTimestamp)
                BOOST_CHECK_EQUAL(prevChunkFinalTimestamp + 1, thisChunkInitialTimestamp);
        }
    }


    BOOST_AUTO_TEST_CASE(timestamp_dataset_dir_monotony) {     // Are timestamps sequential?
        // Create parser
        auto parser = new FTDCParser();


        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        //parser->keepChunkStructures(true);

        auto status = parser->parseFiles(&fileList, false, false);
        BOOST_CHECK_EQUAL(status, 0);

        auto chunkVector = parser->getChunks();

        BOOST_CHECK_GT(chunkVector.size(), 1);

        for (int i = 1; i < chunkVector.size(); ++i) {
            auto prevChunkFinalTimestamp = chunkVector[i - 1]->getEnd() / 1000;
            auto thisChunkInitialTimestamp = chunkVector[i]->getStart() / 1000;

            if (prevChunkFinalTimestamp + 1 != thisChunkInitialTimestamp)
                BOOST_CHECK_EQUAL(prevChunkFinalTimestamp + 1, thisChunkInitialTimestamp);
        }
    }


    BOOST_AUTO_TEST_CASE(dataSetMonotony) {
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);

        BOOST_CHECK_EQUAL(status, 0);

        auto ts = parser->getMetric("start");

        uint64_t prevTimestamp = (*ts)[0] / 1000;
        uint64_t thisTimestamp;
        for (int i = 1; i < ts->size(); ++i) {

            thisTimestamp = (*ts)[i] / 1000;

            if (prevTimestamp + 1 != thisTimestamp)
                BOOST_CHECK_EQUAL(prevTimestamp + 1, thisTimestamp);

            prevTimestamp = thisTimestamp;
        }
        BOOST_CHECK_EQUAL(1, 1);


    }

    BOOST_AUTO_TEST_CASE(metrics) {     // Are there metrics here?
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> files;

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);
        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        for (auto mn: metricNames) {
            BOOST_TEST_MESSAGE(mn);
        }
        BOOST_TEST_MESSAGE(msg);
    }

    BOOST_AUTO_TEST_CASE(matrix_full) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);

        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        auto ts = parser->getMetric("start");
        auto m1 = parser->getMetric(metricNames[1]);
        auto m2 = parser->getMetric(metricNames[3]);
        auto m3 = parser->getMetric(metricNames[5]);
        auto m4 = parser->getMetric(metricNames[7]);

        msg = str( boost::format("Timestamp has %1% elements\n%2%:%3%\n%4%:%5%\n%6%:%7%\n%8%:%9%\n") % ts->size() %
                metricNames[1] % m1->size() %
                metricNames[3] % m2->size() %
                metricNames[5] % m3->size() %
                metricNames[7] % m4->size() );
        BOOST_TEST_MESSAGE(msg);
    }


    BOOST_AUTO_TEST_CASE(timestamps) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);

        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();

        auto ts = parser->getMetric("start");

        auto half_ts = (*ts)[ts->size()/2];

        auto first_half  = parser->getMetric("start",INVALID_TIMESTAMP, half_ts);
        auto second_half = parser->getMetric("start", half_ts,INVALID_TIMESTAMP);
        auto first_half_size = first_half->size();
        auto second_half_size = second_half->size();

        auto msg = str(boost::format("Samples in start metric is %1%. First half is %2%, second half is %3%")
                % ts->size() % first_half_size % second_half_size);
        BOOST_TEST_MESSAGE(msg);

        BOOST_CHECK_GT(first_half_size, 0);
        BOOST_CHECK_GT(second_half_size, 0);

        BOOST_CHECK_EQUAL(ts->size(), first_half_size+second_half_size);


        // Test case: all in one chunk:
        auto ten_more = (*ts)[(ts->size()/2) + 10];
        auto ten_elements = parser->getMetric("start", half_ts, ten_more );

        BOOST_CHECK_EQUAL(ten_elements->size(), 10);

        // Test case: across two chunks
        auto four_hundred =  (*ts)[(ts->size()/2) + 400];
        auto four_hundred_elements = parser->getMetric("start", half_ts, four_hundred );

        BOOST_CHECK_EQUAL(four_hundred_elements->size(), 400);
    }


    BOOST_AUTO_TEST_CASE(matrix_with_timestamps) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);

        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        auto ts = parser->getMetric("start");

        auto start_ts = (*ts)[ts->size()/2];
        auto end_ts = (*ts)[ts->size()/2 + 1100];

        auto m1 = parser->getMetric(metricNames[1], start_ts, end_ts);
        auto m2 = parser->getMetric(metricNames[3], start_ts, end_ts);
        auto m3 = parser->getMetric(metricNames[5], start_ts, end_ts);
        auto m4 = parser->getMetric(metricNames[7], start_ts, end_ts);

        msg = str( boost::format("Start timestamp %1%, end timestamp %2%.  Elements\n%3%:%4%\n%5%:%6%\n%7%:%8%\n%9%:%10%\n") %
                 start_ts % end_ts %
                   metricNames[1] % m1->size() %
                   metricNames[3] % m2->size() %
                   metricNames[5] % m3->size() %
                   metricNames[7] % m4->size()
                   );
        BOOST_TEST_MESSAGE(msg);
    }

    BOOST_AUTO_TEST_CASE(file_info) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false);

        BOOST_CHECK_EQUAL(status, 0);

        auto fi = parser->getParsedFileInfo();
        for (auto f : fi) {

            auto msg = str( boost::format("File %1%: samples %2%.  Start timestamp: %3%. End timestamp: %4%") %
                               f->getFileAbsolute() %
                               f->getSamplesCount() %
                               f->getStart() %
                               f->getEnd()
            );
            BOOST_TEST_MESSAGE(msg);

        }

    }


    // - - - -

    BOOST_AUTO_TEST_CASE(lazy_parser) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, true);

        BOOST_CHECK_EQUAL(status, 0);

        auto fi = parser->getParsedFileInfo();
        for (auto f : fi) {

            auto msg = str( boost::format("File %1%: samples %2%.  Start timestamp: %3%. End timestamp: %4%") %
                            f->getFileAbsolute() %
                            f->getSamplesCount() %
                            f->getStart() %
                            f->getEnd()
            );
            BOOST_TEST_MESSAGE(msg);
        }

        auto chunkVector = parser->getChunks();
        auto pChunk = chunkVector[0];

        // We construct the metrics. These are name and first value only since deltas have not been read.
        pChunk->Consume();
    }


    BOOST_AUTO_TEST_CASE(lazy_parser_pudding) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, true);

        BOOST_CHECK_EQUAL(status, 0);

        auto fi = parser->getParsedFileInfo();
        for (auto f : fi) {

            auto msg = str( boost::format("File %1%: samples %2%.  Start timestamp: %3%. End timestamp: %4%") %
                            f->getFileAbsolute() %
                            f->getSamplesCount() %
                            f->getStart() %
                            f->getEnd()
            );
            BOOST_TEST_MESSAGE(msg);
        }

        auto metricNames = parser->getMetricsNames();
        BOOST_CHECK_GT(metricNames.size(), 0);

        auto ts = parser->getMetric("start");

        auto half_ts = (*ts)[ts->size()/2];

        auto first_half  = parser->getMetric("start",INVALID_TIMESTAMP, half_ts);
        auto second_half = parser->getMetric("start", half_ts, INVALID_TIMESTAMP);
        auto first_half_size = first_half->size();
        auto second_half_size = second_half->size();

        auto msg = str(boost::format("Sample count in 'start' metric is %1%. First half is %2%, second half is %3%")
                       % ts->size() % first_half_size % second_half_size);
        BOOST_TEST_MESSAGE(msg);

        // Test case: all in one chunk:
        auto ten_more = (*ts)[(ts->size()/2) + 10];
        auto ten_elements = parser->getMetric("start", half_ts, ten_more );

        BOOST_CHECK_EQUAL(ten_elements->size(), 10);

        // Test case: across two chunks
        auto four_hundred =  (*ts)[(ts->size()/2) + 400];
        auto four_hundred_elements = parser->getMetric("start", half_ts, four_hundred );

        BOOST_CHECK_EQUAL(four_hundred_elements->size(), 400);
    }


    BOOST_AUTO_TEST_CASE(matrix_with_timestamps_lazy) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, true);

        BOOST_CHECK_EQUAL(status, 0);

        auto metricNames = parser->getMetricsNames();
        auto msg = str(boost::format("Metric count is %1%") % metricNames.size());
        BOOST_TEST_MESSAGE(msg);

        auto ts = parser->getMetric("start");

        auto start_ts = (*ts)[ts->size()/2];
        auto end_ts = (*ts)[ts->size()/2 + 1100];

        auto m1 = parser->getMetric(metricNames[1], start_ts, end_ts);
        auto m2 = parser->getMetric(metricNames[3], start_ts, end_ts);
        auto m3 = parser->getMetric(metricNames[5], start_ts, end_ts);
        auto m4 = parser->getMetric(metricNames[7], start_ts, end_ts);

        msg = str( boost::format("Start timestamp %1%, end timestamp %2%.  Elements\n%3%:%4%\n%5%:%6%\n%7%:%8%\n%9%:%10%\n") %
                   start_ts % end_ts %
                   metricNames[1] % m1->size() %
                   metricNames[3] % m2->size() %
                   metricNames[5] % m3->size() %
                   metricNames[7] % m4->size()
        );
        BOOST_TEST_MESSAGE(msg);
    }


    BOOST_AUTO_TEST_CASE(rated_metrics) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, true);

        BOOST_CHECK_EQUAL(status, 0);

        auto connCreated_ampersand = parser->getMetric("@serverStatus.connections.totalCreated");
        auto connCreated_flag      = parser->getMetric("serverStatus.connections.totalCreated",  INVALID_TIMESTAMP,INVALID_TIMESTAMP, true);
        auto connCreated_raw       = parser->getMetric("serverStatus.connections.totalCreated");

        BOOST_CHECK_EQUAL(connCreated_ampersand->size(), connCreated_flag->size());
    }


    BOOST_AUTO_TEST_CASE(numpy_lists_lazy) {

        std::vector<std::string> ftdc_metric_keys;

        ftdc_metric_keys.emplace_back( "start");
        // When starting with @ apply a rated differential
        // WT tickets
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.read.out");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.write.out");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.read.totalTickets");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.write.totalTickets");

        // application threads
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.checkpoint lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.dhandle lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.durable timestamp queue lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.metadata lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.read timestamp queue lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.schema lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.table lock application thread time waiting for the table lock (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow cursor application thread wait time (usecs)");
        // global WT lock acquistions
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global read lock acquisitions");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex shared lock read-lock calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex shared lock write-lock calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex condition wait calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.transaction.transaction range of IDs currently pinned");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.transaction.transaction range of IDs currently pinned by a checkpoint");

        // internal threads
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.checkpoint lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.dhandle lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.metadata lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.durable timestamp queue lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.read timestamp queue lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.schema lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.table lock internal thread time waiting for the table lock (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global lock internal thread time waiting (usecs)");

        // capacities? learning how these work as a function of available CPU time (what domain?)...
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting due to total capacity (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during checkpoint (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during eviction (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during logging (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during read (usecs)");

        // cache, full-ness & pressure - unrated
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.tracked dirty bytes in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes currently in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes dirty in the cache cumulative");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes not belonging to page images in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes belonging to the cache overflow table in the cache");

        // cache, storage demand & pressure
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.bytes read into cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.bytes written from cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.total read I/Os");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.total write I/Os");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.block-manager.bytes read");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.block-manager.bytes written");

        // checkpoint pressure
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.transaction.transaction checkpoint currently running");  // unrated
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.connection.files currently open");  // unrated
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.eviction worker thread evicting pages");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.hazard pointer check calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cursor.cursor search near calls");

        // overflow / lookaside pressure (on host demand) pre-4.4
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow score");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table entries");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table insert calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table remove calls");

        // "@serverStatus.wiredTiger.cache.cache overflow cursor internal thread wait time (usecs)"
        // new in 4.4:
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store score");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table on-disk size");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table insert calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table reads");

        ftdc_metric_keys.emplace_back("@local.oplog.rs.stats.wiredTiger.reconciliation.overflow values written");
        ftdc_metric_keys.emplace_back("@local.oplog.rs.stats.wiredTiger.btree.overflow pages");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.overflow pages read into cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.pages selected for eviction unable to be evicted as the parent page has overflow items");

        // WT backup cursors
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.backupCursorOpen");
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.oldestRequiredTimestampForCrashRecovery.t");
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.oldestRequiredTimestampForCrashRecovery.i");

        // dhandles
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.data-handle.connection data handles currently active");

        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, true);

        auto metricList = parser->getMetric(ftdc_metric_keys);

        BOOST_CHECK_EQUAL(metricList.size(), ftdc_metric_keys.size());

        int i = 0;
        for (auto m : metricList) {

            if (m) {
                BOOST_CHECK_GT(m->size(), 0);
            }
            else {

                auto msg = str( boost::format("Name '%1%'  not found in metrics") % ftdc_metric_keys[i]);

                BOOST_TEST_MESSAGE(msg);
            }
            ++i;
        }
    }


    BOOST_AUTO_TEST_CASE(numpy_matrix_lazy) {

        std::vector<std::string> ftdc_metric_keys;

        ftdc_metric_keys.emplace_back( "start");
        // When starting with @ apply a rated differential
        // WT tickets
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.read.out");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.write.out");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.reaMd.totalTickets");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.concurrentTransactions.write.totalTickets");

        // application threads
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.checkpoint lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.dhandle lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.durable timestamp queue lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.metadata lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.read timestamp queue lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.schema lock application thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.table lock application thread time waiting for the table lock (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global lock application thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow cursor application thread wait time (usecs)");
        // global WT lock acquistions
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global read lock acquisitions");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex shared lock read-lock calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex shared lock write-lock calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.pthread mutex condition wait calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.transaction.transaction range of IDs currently pinned");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.transaction.transaction range of IDs currently pinned by a checkpoint");

        // internal threads
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.checkpoint lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.dhandle lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.metadata lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.durable timestamp queue lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.read timestamp queue lock internal thread time waiting (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.schema lock internal thread wait time (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.table lock internal thread time waiting for the table lock (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.lock.txn global lock internal thread time waiting (usecs)");

        // capacities? learning how these work as a function of available CPU time (what domain?)...
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting due to total capacity (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during checkpoint (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during eviction (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during logging (usecs)");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.capacity.time waiting during read (usecs)");

        // cache, full-ness & pressure - unrated
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.tracked dirty bytes in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes currently in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes dirty in the cache cumulative");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes not belonging to page images in the cache");
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.cache.bytes belonging to the cache overflow table in the cache");

        // cache, storage demand & pressure
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.bytes read into cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.bytes written from cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.total read I/Os");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.connection.total write I/Os");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.block-manager.bytes read");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.block-manager.bytes written");

        // checkpoint pressure
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.transaction.transaction checkpoint currently running");  // unrated
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.connection.files currently open");  // unrated
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.eviction worker thread evicting pages");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.hazard pointer check calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cursor.cursor search near calls");

        // overflow / lookaside pressure (on host demand) pre-4.4
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow score");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table entries");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table insert calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.cache overflow table remove calls");

        // "@serverStatus.wiredTiger.cache.cache overflow cursor internal thread wait time (usecs)"
        // new in 4.4:
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store score");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table on-disk size");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table insert calls");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.history store table reads");

        ftdc_metric_keys.emplace_back("@local.oplog.rs.stats.wiredTiger.reconciliation.overflow values written");
        ftdc_metric_keys.emplace_back("@local.oplog.rs.stats.wiredTiger.btree.overflow pages");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.overflow pages read into cache");
        ftdc_metric_keys.emplace_back("@serverStatus.wiredTiger.cache.pages selected for eviction unable to be evicted as the parent page has overflow items");

        // WT backup cursors
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.backupCursorOpen");
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.oldestRequiredTimestampForCrashRecovery.t");
        ftdc_metric_keys.emplace_back("serverStatus.storageEngine.oldestRequiredTimestampForCrashRecovery.i");

        // dhandles
        ftdc_metric_keys.emplace_back("serverStatus.wiredTiger.data-handle.connection data handles currently active");

        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR)) {
            fileList.push_back(fileInPath.path().string());
            break; // only one
        }

        auto status = parser->parseFiles(&fileList, false, false, true);
        auto fi = parser->getParsedFileInfo();
        for (auto f : fi) {

            auto msg = str( boost::format("File %1%: samples %2%.  Start timestamp: %3%. End timestamp: %4%") %
                            f->getFileAbsolute() %
                            f->getSamplesCount() %
                            f->getStart() %
                            f->getEnd()
            );
            BOOST_TEST_MESSAGE(msg);
        }

        //
        size_t stride = 0;
        auto matrix = parser->getMetricMatrix(ftdc_metric_keys, &stride);
        auto ts = parser->getMetric("start");

        auto msg = str( boost::format("Size is %1%") % matrix->size() );
        BOOST_TEST_MESSAGE(msg);

        BOOST_CHECK_EQUAL( matrix->size(), ftdc_metric_keys.size()*ts->size());
    }

    BOOST_AUTO_TEST_CASE(get_json) {
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        auto status = parser->parseFiles(&fileList, false, false, false);
        auto p = parser->getJsonAtPosition(1);

        BOOST_TEST_MESSAGE(p);

    }

    BOOST_AUTO_TEST_CASE(dump_json_ts) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        const std::string s =  "./output_ts.json";
        auto ret = parser->dumpDocsAsJsonTimestamps(fileList[0], s, INVALID_TIMESTAMP, INVALID_TIMESTAMP );

        BOOST_CHECK_GT(ret, 0);
    }

    BOOST_AUTO_TEST_CASE(dump_csv_ts) {     //
        // Create parser
        auto parser = new FTDCParser();

        std::vector<std::string> fileList;
        for (auto &&fileInPath: std::filesystem::directory_iterator(DATA_TEST_DIR))
            fileList.push_back(fileInPath.path().string());

        const std::string s =  "./output_ts.csv";
        auto ret = parser->dumpDocsAsCsvTimestamps(fileList[0], s, INVALID_TIMESTAMP, INVALID_TIMESTAMP );

        BOOST_CHECK_GT(ret, 0);
    }

BOOST_AUTO_TEST_SUITE_END()

