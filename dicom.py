import json

import pydicom as dicom
import os


class Dicom:
    def __init__(self, folder):
        self.folder = folder

    def get_files_names(self) -> list:
        files_list = os.listdir(self.folder)
        return files_list

    def read_dcm(self) -> list:
        meta_list = list()
        for dcm_name in self.get_files_names():
            path = f'./src/{dcm_name}'
            dcm_view = dicom.dcmread(path)
            meta_list.append(dcm_view)
        return meta_list

    def anonymous_and_make_data_json(self, patient_name='anonymous', new_folder='updated_files'):
        my_list_json = list()
        dict_for_json = dict()
        my_cwd = os.getcwd()
        os.mkdir(f'{my_cwd}/{new_folder}')
        for dcm_name in self.get_files_names():
            path = f'./src/{dcm_name}'
            dcm_view = dicom.dcmread(path)
            dcm_view.PatientName = patient_name
            new_file_name = f'{dcm_view.SOPInstanceUID.title()}.dcm'
            path_for_save = f'{my_cwd}/{new_folder}/{dcm_view.StudyInstanceUID.title()}/{dcm_view.SeriesInstanceUID.title()}'
            os.makedirs(path_for_save, exist_ok=True)
            way = os.path.join(path_for_save, new_file_name)
            dcm_view.save_as(way)
            dict_for_json[path] = way
            my_list_json.append(dict_for_json)
        with open('inf.json', 'a', encoding='utf-8') as file:
            json.dump(my_list_json, file)


my_dicom = Dicom('src')
my_dicom.anonymous_and_make_data_json()
