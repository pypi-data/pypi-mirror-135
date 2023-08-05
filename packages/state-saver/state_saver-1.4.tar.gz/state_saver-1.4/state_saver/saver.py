import os
from datetime import datetime
from shutil import copyfile


class SourceSaver:
    def __init__(self, target_dir, 
                        extensions_filter=None, 
                        include_subdirs=False,
                        current_file_only=False,
                        basic_folder_identifier="Saver__",
                        saver_folder_datetime_format="%Y%m%d",
                        avoid_saving_already_saved_files=True,
                        whitelist_filenames=None,
                        blacklist_filenames=None):
        """
        Args:
            target_dir, [string] - a folder where the files will be saved
            extensions_filter, [list] - a list of extensions to include in saving. Example: ['py', 'txt'], default: None- meaning that all files will be saved. If empty list is passed, no files will be saved
            include_subdirs, [bool] - if True, the subdirectories will be included in the saving
            current_file_only, [bool] - if True, only the current file will be saved
            saver_folder_datetime_format, [string] - a format of the output folder name -timestamp. Example: "%Y %m %d"
            basic_folder_identifier, [string] - First part of the folder name that will be added to the target_dir. Example: "Saver__"
            avoid_saving_already_saved_files, [bool] - if True, the files that are already saved will not be saved again
            whitelist_filenames, [list] - a list of filenames that will be saved. Names only. Example: ['file1.txt', 'file2.txt']. Setting this parameter will override the extensions_filter
            blacklist_filenames, [list] - a list of filenames that will not be saved. Names only. Example: ['file1.txt', 'file2.txt']. Setting this parameter will override the whitelist_filenames if matches are found
        
        Example usage:
            SourceSaver(target_dir='test_saving', 
                extensions_filter=['py', 'txt'], 
                include_subdirs=False,
                current_file_only=True,
                basic_folder_identifier="KorBaby__",
                saver_folder_datetime_format="%Y%m%d",
                avoid_saving_already_saved_files=True,
                whitelist_filenames=['damn.tx'],
                blacklist_filenames=['saver.py'])
        """
        self.base_dir = os.getcwd()
        self.target_dir = target_dir
        self.include_subdirs = include_subdirs
        self.folder_datetime_format = saver_folder_datetime_format
        self.extensions_filter = extensions_filter
        self.current_file_only = current_file_only
        self.avoid_saving_already_saved_files = avoid_saving_already_saved_files
        self.whitelist_filenames = whitelist_filenames
        self.blacklist_filenames = blacklist_filenames

        self.basic_saver_identifier = basic_folder_identifier
        self.save_dir_identifier = self.basic_saver_identifier + self._get_timestamp()
        self._process()


    def _get_timestamp(self):
        now = datetime.now()
        timestamp = now.strftime(self.folder_datetime_format)
        return timestamp

        
    def filter_extensions(self):
        if self.extensions_filter is None:
            return None

        updated_list_ext = []
        for ext in self.extensions_filter:
            new_ext = ext.replace('.', '').replace('*', '')
            new_ext = '.' + new_ext
            updated_list_ext.append(new_ext)
        return updated_list_ext


    def _get_files_list(self):
        """
        Returns a list of files in the target directory
        """
        file_paths = []
        extensions = self.filter_extensions()

        if self.current_file_only:
            file_paths.append(os.path.join(self.base_dir, __file__))
        else:
            if self.include_subdirs:
                for root, _, files in os.walk(self.base_dir):
                    for file in files:
                        should_include = None

                        if self.whitelist_filenames is not None and file in self.whitelist_filenames:
                            should_include = True
                        if self.blacklist_filenames is not None and file in self.blacklist_filenames:
                            should_include = False

                        if should_include is None:
                            if extensions is not None:
                                should_include = False
                                for extension in extensions:
                                    if extension in file:
                                        should_include = True
                                        break
                            else:
                                should_include = True

                            if self.avoid_saving_already_saved_files:
                                if self.basic_saver_identifier in root:
                                    should_include = False

                        if should_include is True:
                            file_paths.append(os.path.join(root, file))
            else:
                for file in [f for f in os.listdir(self.base_dir) if os.path.isfile(f)]:
                    should_include = None
                    if self.whitelist_filenames is not None and file in self.whitelist_filenames:
                        should_include = True
                    if self.blacklist_filenames is not None and file in self.blacklist_filenames:
                        should_include = False
                    
                    if should_include is None:
                        if extensions is not None:
                            should_include = False
                            for extension in extensions:
                                if extension in file:
                                    should_include = True
                                    break
                        else:
                            should_include = True

                    if should_include:
                        file_paths.append(os.path.join(self.base_dir, file))

        return file_paths


    def _process(self):
        """
        Processes the files and subdirectories in the target directory
        """
        try:
            save_dir = os.path.join(self.target_dir, self.save_dir_identifier)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            file_paths = self._get_files_list()
            print("State Saver - saving [{}] files in '{}'".format(len(file_paths), save_dir))
            for file_path in file_paths:
                sub_dir = file_path[len(self.base_dir) + 1:]
                
                from_dir = file_path
                to_dir = os.path.join(save_dir, sub_dir)

                cur_file_dir = os.path.dirname(to_dir)
                if not os.path.exists(cur_file_dir):
                    os.makedirs(cur_file_dir)

                copyfile(from_dir, to_dir)

        except Exception as e:
            print("Unable to save data. Details:\n", e)

        

        
if __name__ == "__main__":
    SourceSaver(target_dir='test_saving', 
                extensions_filter=['py', 'txt'], 
                include_subdirs=False,
                current_file_only=True,
                basic_folder_identifier="KorBaby__",
                saver_folder_datetime_format="%Y%m%d",
                avoid_saving_already_saved_files=True,
                whitelist_filenames=['damn.tx'],
                blacklist_filenames=['saver.py'])