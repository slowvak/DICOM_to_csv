
#!python3
# 
import pydicom
import os
import csv
import sys

# from https://github.com/pydicom/pydicom/blob/master/pydicom/_dicom_dict.py
TagList = ['FileName','StudyDate', 'SeriesDate', 'AcquisitionDate', 'AcquisitionDateTime','StudyTime','SeriesTime', 'AcquisitionTime', 'Modality', \
    'AnatomicRegionsInStudyCodeSequence', 'Manufacturer', 'StationName', 'StudyDescription', 'ProcedureCodeSequence', 'SeriesDescription', \
    'ManufacturerModelName', 'AnatomicRegionSequence', 'AcquisitionContrast', 'PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex', \
    'PatientAge', 'OpticalMagnificationFactor', 'ContrastBolusAgent', 'BodyPartExamined', 'ScanningSequence', 'SequenceVariant',  'ScanOptions', \
    'MRAcquisitionType', 'SequenceName', 'AngioFlag', 'Radiopharmaceutical', 'SliceThickness', 'KVP', 'RepetitionTime', 'EchoTime', 'InversionTime', \
    'NumberOfAverages', 'EchoNumbers', 'MagneticFieldStrength', 'SpacingBetweenSlices', 'NumberOfPhaseEncodingSteps', 'DataCollectionDiameter', \
    'EchoTrainLength', 'DateOfSecondaryCapture', 'ProtocolName', 'ContrastBolusRoute', 'TriggerTime', 'ReconstructionDiameter', 'DistanceSourceToDetector', \
    'DistanceSourceToPatient', 'ExposureTime', 'XRayTubeCurrent', 'Exposure', 'ReceiveCoilName', 'TransmitCoilName', 'FlipAngle', 'VariableFlipAngleFlag', \
    'IVUSAcquisition', 'TransducerFrequency', 'TransducerType', 'PulseRepetitionFrequency', 'PulseSequenceName', 'EchoPulseSequence', 'InversionRecovery', \
    'FlowCompensation', 'MultipleSpinEcho', 'PhaseContrast', 'TimeOfFlightContrast', 'Spoiling', 'SteadyStatePulseSequence', 'EchoPlanarPulseSequence', \
    'DiffusionBValue', 'MRSpectroscopyFOVGeometrySequence', 'SlabThickness', 'SlabOrientation', 'RFEchoTrainLength', 'GradientEchoTrainLength',\
    'ASLTechniqueDescription', 'CTAcquisitionTypeSequence', 'AcquisitionType', 'ReconstructionAlgorithm', 'XRayTubeCurrentInmA', 'ExposureInmAs', \
    'ContrastBolusAgentAdministered', 'MultienergyCTAcquisition', 'FunctionalMRSequence', 'USImageDescriptionSequence', 'SeriesNumber', 'AcquisitionNumber',\
    'InstanceNumber', 'ImagePositionPatient', 'ImageOrientationPatient', 'ImagesInAcquisition', 'SliceLocation', 'ImagePositionVolume', 'ImageOrientationVolume',\
    'UltrasoundColorDataPresent', 'PixelSpacing', 'WindowCenter', 'WindowWidth', 'RescaleIntercept', 'RescaleSlope', 'SegmentationType', 'SegmentSequence', \
    'SegmentLabel', 'SegmentDescription', 'SegmentationAlgorithmIdentificationSequence', 'RTImageLabel', 'RTImageName', 'RTImageDescription', 'FractionNumber']


def get_tag_values(fname) -> list:
    """Looks through the dicom header for tags in the DicomDictionary above
       If present, it gets the value, else 'Na'

    Args:
        fname (string): full path to the dicom file
        
    Returns:
        list: list of values for each of the tags in DicomDictionary
    """
    
    try:
        ds = pydicom.dcmread(fname)
    except:
        return None

    tagline = []  # put placeholder for filename
    tagline.append(fname)
    for tag in TagList:
        if tag != 'FileName':
            v = 'Na'
            try:
                elem = ds.data_element(tag)
                v = str(elem.value)
                if v == '':
                    v = 'None'
                else:
                    v = v.replace(",",".")  # make sure no commas in the value
            except:
                pass    
            tagline.append(v)
    return tagline


def makeCSV(dicom_path, output_path) -> None:
    """
    get_tags_in_files iterates over a directory, finds dicom files with
    a .dcm extension, and finds all unique dicom tag instances. it then
    writes the tags out as a csv file.
    Args:
        dicom_path (str): Path to scan for dicom files.
        tag_file_path (str): Path and file name for the output csv file.
    Returns:
        dict: A dictionary containing the tags loaded.
    """

    count = 0
    # Make the first header row in file
    with open(output_path, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields to the first row of file
        csvwriter.writerow(TagList) 
            
        # get the tags
        for root, dir, files in os.walk(dicom_path):
            print (f"Working on {root}/{dir}")
            for f in files:
                fname = os.path.join(root, f)
                row = get_tag_values(fname)
                # write the data rows 
                if row is not None:
                    count = count + 1
                    if count % 500 == 0:
                        print (f"{count} DICOM files processed")
                    csvwriter.writerows([row])
    return 


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        dicom_path = sys.argv[1]  # provide path
    else:
        dicom_path = os.getcwd()  # else uses where it is launched from
    
    output_path = os.path.join (dicom_path, "original_DICOM_tags.csv")
    makeCSV(dicom_path, output_path)