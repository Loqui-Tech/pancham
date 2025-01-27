import pandas as pd

from data_frame_configuration import DataFrameConfiguration

class Reporter:
    """
    Handles the process of reporting the state of operations, including the start,
    error occurrences, and conclusion of specific processes. This class is designed
    to ensure consistent and structured reporting based on input configurations and
    provided data. It supports integration with external monitoring and logging tools
    for enhanced observability.
    """

    def report_start(self, configuration: DataFrameConfiguration):
        """
        Reports the start of a process based on the given configuration.

        :param configuration: Configuration details provided as a DataFrameConfiguration
            object.
        :return: None
        """
        pass

    def report_error(self, error: Exception):
        """
        Reports an error by capturing the given exception.

        This method is used to handle error reporting processes when an exception occurs.
        It facilitates logging, monitoring, or other specified error handling mechanisms.

        :param error: The exception that needs to be reported.
        :type error: Exception
        :return: None
        """
        pass

    def report_end(self, configuration: DataFrameConfiguration, data: pd.DataFrame):
        """
        Generates a report based on the provided configuration and data at the end of a
        specific processing routine. This function is called to finalize and encapsulate
        all relevant information into a structured format specified by the configuration.

        :param configuration: Contains the configuration settings required for generating
            the report. These settings determine the layout, formatting, filters, and
            other properties used during the reporting process.
        :type configuration: DataFrameConfiguration
        :param data: The input data in the form of a pandas DataFrame upon which the
            report is generated. This data represents the final state to be included in
            the report.
        :type data: pd.DataFrame
        :return: Finalized report data or outcomes (can vary based on implementation).
            Expected to provide a structured representation directly derived from the
            configuration and data inputs.
        :rtype: None
        """
        pass

    def report_output(self, data: pd.DataFrame, output: str):
        """
        Reports the given data to the specified output location. The method processes
        the provided DataFrame and produces output formatted as per the requirements.
        The output could be written to a file, database, or another destination
        determined by the `output` parameter.

        :param data: The data to be processed and reported.
        :type data: pandas.DataFrame
        :param output: The destination where the processed data will be written.
        :type output: str
        :return: None
        :rtype: None
        """
        pass

class PrintReporter(Reporter):
    """
    A reporter class for printing updates during file processing.

    This class provides a simple implementation of the Reporter
    interface by printing messages about the process status,
    including the start, errors, and completion, to the standard
    output. It is designed for debugging or quick monitoring of
    the file processing and provides instant feedback on the
    processing state.

    :ivar some_attribute: Provide a description of what this attribute
        represents, its role, etc., if applicable to the parent
        Reporter class.
    :type some_attribute: type
    """

    def report_start(self, configuration: DataFrameConfiguration):
        print(f"Starting processing for {configuration.file_path}")

    def report_error(self, error: Exception):
        print(f"Error processing file: {error}")

    def report_end(self, configuration: DataFrameConfiguration, data: pd.DataFrame):
        print(f"Finished processing for {configuration.file_path} - {len(data)} rows")