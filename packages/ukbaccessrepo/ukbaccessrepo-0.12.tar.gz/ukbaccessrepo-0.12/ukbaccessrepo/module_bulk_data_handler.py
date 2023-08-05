from difflib import get_close_matches
static_resource_path="/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_november_2021/"
import pandas as pd
import datalad
import os
import subprocess

class bulk_data_handler:

    """
    A class to represent family of methods that can handle bulk data retrieval

    ...

    Attributes
    ----------
    columns_to_read_for_field_id : list
        list of relevant columns to read from metadata file


    Methods
    -------
    display_all_ukb_categories():
        displays all the categories

    get_field_ids_for_category(category_name):
        retrieves filed ids for a category

    get_subject_list_field_ids(category_name):
        retrieves list of subject relevant to that field id

    get_data_bulk(field_id,subject_id):
        downloads bulk data from openmind

    """


    def __init__(self):
        self.columns_to_read_for_field_id = []
        return


    def display_all_ukb_categories(self):
        """
        Utility function which lets user see all the major categories present in the UKB dataset. Reads
        categories from a static resource file inside package

        Parameters:
        Needs no parameters to operate

        Returns:
        categories list: List having all the unique categories of UKB
        :rtype: list of strings
        """

        unique_category_file_object = open(static_resource_path+"all_unique_categories.txt", "r")
        all_categories_list = unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return formatted_category_list


    def get_field_ids_for_category(self,category_name):

        """
        A utility function which lets user see the associated field ids for each category, reads from a static file
        containing all the  category names and field ids

        Parameters:
        a string representing a category name

        Returns:
        categories list: pandas object having related field ids of the category
        :rtype: pandas table
        """

        temp_field_ids_df = pd.read_csv(static_resource_path+"ukb_field_ids.csv")
        return temp_field_ids_df[temp_field_ids_df['Category'] == category_name]


    def get_subject_list_field_ids(self,field_id):

        """
        A helper function which lets user see subjects having data related to a field_id. Reads a metadata file
        into a pandas object, only reading relevant coloumns because of size of the csv file

        Parameters:
        a int representing a field id

        Returns:
        subject list: a list of subject ids
        :rtype: list
        """

        with open(static_resource_path+'new_column_list_1.txt') as f:
            columns_list_df1 = f.readlines()

        for column_name in columns_list_df1:
            if int(column_name.split("-")[0]) == field_id:
                self.columns_to_read_for_field_id.append(column_name.strip())

        tempdf=pd.read_csv(static_resource_path+"ukb49570.csv", usecols=self.columns_to_read_for_field_id+['eid'])

        return tempdf['eid'].unique()


    def get_data_bulk(self, field_id,subject_id):
        """
        A helper function which lets user download bulk data related to a subject, invokes datalad under the hood
        download starts after user provides credentials in a new terminal shell

        Parameters:
        integers representing field id and subject id

        Returns:
        download path string: path where bulk data has been downloaded
        :rtype: str
        """

        str_subject_id=str(subject_id)
        sting_for_datalad_command=""
        for col in self.columns_to_read_for_field_id:
            modified_col=col.replace('-','_').replace('.', '_')
            temp_str=str_subject_id+"/"+str_subject_id+"_"+modified_col+".zip"+" "
            sting_for_datalad_command+=temp_str
        print(sting_for_datalad_command)


        #tempdf = pd.read_csv("/media/tighu/extended_storage/ukb49570.csv", usecols=self.columns_to_read_for_field_id+['eid'])
        os.system("interact")
        # os.chdir('/ocean/projects/asc170022p/tighu/ukb/inputs/{}'.format(str_subject_id))
        # os.system("git config remote.origin.annex-ignore false")
        # os.chdir('/ocean/projects/asc170022p/tighu/ukb/inputs/')
        # os.system("datalad get {}".format(sting_for_datalad_command))


        return "/ocean/projects/asc170022p/tighu/ukb/inputs/"+str_subject_id


    def search_category_by_name(self,query):


        """
        A helper function which return closest matching category based on query given by user,
        uses built in funtion to get close match

        Parameters:
        query about the category name, probablity threshold can also be provided as an additional parameter

        Returns:
        list: a list with close matching categories name

        """

        unique_category_file_object = open("all_unique_categories.txt","r")
        all_categories_list=unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return get_close_matches(query, formatted_category_list, 5, 0.3)

    def check_bulk_data_size(self,subject_id_list,field_id_list):
        """
        Simple Utility function to keep tabs on the bulk data bieng fetched

        Parameters:
        subject_id_list: list with subject ids
        field_id_list: list with field ids that need to fetched for each subject

        Returns:
        bulk_files_size_estimates: Binary string of the sum of a and b
        :rtype: int
        """
        # get an estimate of bulk data files if they are needed to be fetched from openmind
        # to make sure we arent downloading excessive data from a different cluster

        return "bulk_files_size_estimates"

    def get_bulk_data_batch(self,ukb_object_list,**kwargs):
        # process the object ukb_object_list
        # make chained/parallel calls datalad calls if copy not on our cluster
        # return the a dictionary with key as subject_id+field_id and path of metadata file as value
        return "subject_dict"

    def check_location_bulk_data(self, subject_id,field_id):
        # check if we have the bulk data files in our cluster or are they only on openmind
        #set flag accordingly and return flags
        return "flag_location"

    def check_valid_subject_field_id(self,subject_id,field_id):
        #check whether the following field id exists for this subjct or not
        # if not make the user aware of the case and return flag
        return "valid_field_id_flag"



    def perform_subject_field_ids_tally(self,subject_id_list,field_id_list):
        # check to perform subject and field level tally across the two clusters and ouput how many subject and field_ids are present
        # in each

        return "subject_and_field_id_counts"
