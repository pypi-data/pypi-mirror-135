from .Logger import *
import os

class PickleLogger(Logger):
    """Modification of Logger that saves the numpy arrays as different files

    This logger leads to faster saving and loading, but generates more files.
    What is more those files are not readable for humans.
    """
    def __init__(self, file='optimizer.log', what_to_log=None, optimizer_name='DE'):
        """Initialise the Logger

        Parameters
        ----------
        file: string
            The file to which the logged information will be provided.
            Additional files will be saved in a folder with the same name as the file
            without extension followed by "_objects". If such a folder already exist,
            the additional subsequent number is added.
            For example, when file='optimizer.log', then the folder will be 'optimizer_objects', or
            if such a folder already exists, 'optimizer_objects0' and then 'optimizer_objects1' and so on.
        what_to_log: list, optional
            When provided, only the subset of the what_to_log list will be logged. Other information
            will not be logged.
            Useful when only some information is needed to speed up the process of logs gathering and
            make the log files take less place on hard drive.
        optimizer_name: string
            The name that will be logged on the beginning of the log with an "info" tag.
        """
        super().__init__(file=file, what_to_log=what_to_log, optimizer_name=optimizer_name)
        absolute_path = os.path.relpath(file)
        dir_name_candidate, ext = os.path.splitext(absolute_path)
        dir_name_candidate += '_objects'
        if os.path.exists(dir_name_candidate):
            dir_name_suffix=0
            while os.path.exists(dir_name_candidate+str(dir_name_suffix)):
                dir_name_suffix += 1
            dir_name_candidate=dir_name_candidate+str(dir_name_suffix)
        self.dir_for_arrays=dir_name_candidate
        os.mkdir(self.dir_for_arrays)
        self.generation_count=0
        self.batch_dict={}

    def _log(self, name, info, array=None):
        if self.what_to_log is not None and not name in self.what_to_log:
            return
        if array is None:
            array = name in self.array_variables
        if array:
            self.batch_dict[name]=info
            info = self._get_filepath_for_nparray(rel_to_logfile=True)
        super()._log(name, info, array=False)

    def _start_generation(self, generations_done, generations_after_last_restart):
        self._log_batch()
        super()._start_generation(generations_done, generations_after_last_restart)

    def _restarting(self, generations_after_last_restart, current_best_f):
        self._log_batch()
        super()._restarting(generations_after_last_restart, current_best_f)

    def _log_batch(self):
        filepath = self._get_filepath_for_nparray()
        np.savez_compressed(filepath, **self.batch_dict)
        self.batch_dict={}
        self.generation_count += 1

    def _get_filepath_for_nparray(self, rel_to_logfile=False):
        filename = 'gen' + str(self.generation_count) + '.npz'
        if rel_to_logfile:
            dirname = os.path.basename(self.dir_for_arrays)
        else:
            dirname = self.dir_for_arrays
        filepath = os.path.join(dirname, filename)
        return filepath


class PickleLogReader(LogReader):
    """
    Read logs created with *PickleLogger*.

    Warnings
    -----
    Log consists of 1) a \*.log file and 2) \*_objects folder with many gen\*.npy files.
    Log as a whole can be moved and accessed with PickleLogReader from any folder, but log's inner structure must be preserved.

    Example
    --------
    >>> import delo
    >>> import numpy as np
    >>>
    >>> def square(x):
    ...     return np.sum(x ** 2, axis=1)
    >>>
    >>> file_name = 'square_opt.log'
    >>> logger = delo.PickleLogger(file=file_name)
    >>>
    >>> described_function = delo.DescribedFunction(square, dimension=2, domain_lower_limit=-10, domain_upper_limit=10)
    >>> algorithm = delo.DElo(10, logger=logger)
    >>>
    >>> algorithm.optimize(described_function, rng_seed=2022)
    >>>
    >>> logreader = delo.PickleLogReader(file_name)
    >>> best_fs = logreader.read_variable('current_best_f')
    Looking for current_best_f in log file
    Found 100 occurences of `current_best_f`.
    >>> print(best_fs[:5])
    [27.935020304146946, 13.606498015936902, 4.37874090480261, 2.9852266609374456, 0.29795569609533]
    """
    def __init__(self, file):
        """
        Constructor

        Parameters
        ----------
        file : string
            path to \*.log file created with ``LogReader``.

        """
        super().__init__(file=file)
        dir_name = os.path.dirname(file)
        self.log_root_name = dir_name

    def _process_line(self, line, type_name):

        # Structure of lines in file:
        # DEBUG ; 2021-11-14 20:52:34,979 ; restart_eps_x ; None
        # Loglevel ; time ; name ; value

        splitted = line.split(' ; ')
        if len(splitted) != 4:
            raise Exception('Line not processed')
        variable_name = splitted[2]
        raw_value = splitted[3]
        file_name_candidate = os.path.join(self.log_root_name, raw_value[:-1])
        if type_name == 'np.array' and os.path.isfile(file_name_candidate):
            with np.load(file_name_candidate) as data:
                parsed_value = data[variable_name]
        else:
            parsed_value = self._parse_value(raw_value, type_name)
        return {'levelname': splitted[0],
                'asctime': time.strptime(splitted[1], "%Y-%m-%d %H:%M:%S,%f"),
                'variable_name': variable_name,
                'variable_value': parsed_value}


