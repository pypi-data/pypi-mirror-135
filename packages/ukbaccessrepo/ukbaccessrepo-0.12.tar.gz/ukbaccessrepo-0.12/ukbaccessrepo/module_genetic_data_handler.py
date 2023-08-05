import pandas as pd
import pandas_plink
import numpy as np
from pandas_plink import read_plink1_bin

genetic_data_path = "/ocean/projects/asc170022p/tighu/UKB_Genetic_Data/"


class genetic_data_handler:
    """
    A class to represent family of methods that can fetch pandas object based on subject id

    ...

    Attributes
    ----------
    number_of_subjects : int
        number of subjects to fetch genetic data for

    Methods
    -------
    get_genetic_data_batch(number_of_subjects,chromosome_number_list):
        get pandas object having genetic data corresponding to the specified chromosome for specified number of subjects

    """

    def __init__(self):

        self.subjects = np.ndarray
        self.location = np.ndarray

    def get_subject_id(self):
        """
        A utility function which lets user fetch numpy array containing the list of all subject ids

        Parameters:
        No parameter required

        Returns:
        categories list: A numpy array object
        :rtype: np.ndarray
        """
        if self.subjects is None:
            print("Please initialize with a chromosome and read the binary data first")
            return None

        else:
            return self.subjects

    def get_all_genetic_data_storage_location(self):
        """
        A utility function which lets user see all the genetic data locations

        Parameters:
        No parameter required

        Returns:
        categories list: A string
        :rtype: str
        """

        return genetic_data_path


    def get_genetic_locations(self):
        """
        A utility function which lets user fetch numpy array containing the locations of genetic data

        Parameters:
        No parameter required

        Returns:
        categories list: A numpy array object
        :rtype: np.ndarray
        """

        if self.location is None:
            print("Please initialize with a chromosome and read the binary data first")
            return None

        else:
            return self.location


    def get_genetic_binary_data(self, chr_num):
        """
        A utility function which lets user fetch the genetic data associated with a chromosome number

        Parameters:
        a string representing a chromosome of interest

        Returns:
        categories list: pandas object having genetic data of a particular chromosome type
        :rtype: pandas plink table
        """
        genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + chr_num + "_b0_v2.bed",
                                     genetic_data_path + "bim_files/" + "ukb_snp_chr" + chr_num + "_v2.bim",
                                     genetic_data_path + "fam_files/" + "ukb22418_c" + chr_num + "_b0_v2_s488176.fam",
                                     verbose=True)

        self.subjects = genetic_df.sample.values
        self.location = genetic_df.pos.values
        return genetic_df
