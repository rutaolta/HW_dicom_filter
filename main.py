import pydicom as dicom
import os
import shutil
from pathlib import PureWindowsPath, Path
import json


def proper_file(dcm, clause):
    for key, value in dict(clause).items():
        if not(str(value) in dcm[key].value):
            return False
    # str(ds.Modality) == 'CT' and str(ds.ConvolutionKernel) == 'LUNG':
    # and (str(ds.SliceThickness) == '1.5' or str(ds.SliceThickness) == '1.500'):
    # and (str(ds.BodyPartExamined == 'CHEST') or str(ds.BodyPartExamined) == 'ABDOMEN')
    # and str(ds.PatientOrientation) == "['L', 'P']"
    return True


def filter(source_dir, destination_dir, clauses):
    # if not os.path.exists(os.path.join(destination_dir, 'good_series')):
    #     os.mkdir(os.path.join(destination_dir, 'good_series'))

    for root, dirs, files in os.walk(source_dir):
        # print(PureWindowsPath(os.path.basename(root)))
        for f in files:
            # if Path(f).suffix == '.dcm':
            ds = dicom.dcmread(root + '/' + f)
            try:
                # print(PureWindowsPath(os.path.join(root, f)), 'SliceThickness', ds.SliceThickness, 'PatientID', ds.PatientID, 'ConvolutionKernel', ds.ConvolutionKernel)

                if proper_file(ds, clauses):
                    if not os.path.exists(os.path.join(destination_dir, os.path.basename(root))):
                        os.mkdir(os.path.join(destination_dir, os.path.basename(root)))
                    shutil.copy(PureWindowsPath(os.path.join(root, f)),
                                PureWindowsPath(os.path.join(destination_dir, os.path.basename(root), f)),
                                follow_symlinks=True)
            except Exception as e:
                print('Файл {} вызвал ошибку'.format(PureWindowsPath(os.path.join(root, f))), e)


if __name__ == '__main__':
    def get_source_dir():
        source_dir = input('Введите полный путь к папке, где лежат исследования, которые нужно отфильтровать: ') or 'F:\dicom\dicom'
        if not os.path.exists(source_dir):
            print('Введенный путь не существует. Попробуйте еще раз.')
            get_source_dir()
        return source_dir

    def get_destination_dir():
        destination_dir = input('Введите полный путь к папке, куда скопировать подходящее: ') or 'F:\dicom\dicom_f'
        if not os.path.exists(destination_dir):
            print('Введенный путь не существует. Попробуйте еще раз.')
            get_destination_dir()
        return destination_dir

    def parse_to_dir(clauses_input):
        try:
            return json.loads(clauses_input)
        except:
            return ''

    def get_clauses():
        clauses_input = input('Введите условия фильтрации в json-формате: {"00080060":"CT"}: ') or '{"00080060":"MG", "00080080":"РНЦРР"}'
        clauses = parse_to_dir(clauses_input)
        if not bool(clauses):
            print('Невозможно распарсить фильтр. Попробуйте еще раз.')
            get_clauses()
        return clauses

    source_dir = get_source_dir()
    destination_dir = get_destination_dir()
    clauses = get_clauses()
    filter(source_dir, destination_dir, clauses)

    input('FIN')
