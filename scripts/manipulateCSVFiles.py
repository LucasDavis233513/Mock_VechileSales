import pandas as pd

PROGRAMMER_NAME = "Lucas Davis"         # Global Programmer Name

# This class will ask for a list of csv files, were it will then merge them based shared indexs based
#   off a user defined column that is shared among each file.
class mergeCSV:
    _instance = None                    # Variable used to hold the instance of this class

    # Initialize an instance of the class
    def __init__(self):
        raise RuntimeError('Call instance() instead...')
    
    # Singlton method to create an instance of this class
    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance...')
            cls._instance = cls.__new__(cls)

            cls.gatherData()
        
        return cls._instance

    # Gather the data from defined files
    @classmethod
    def gatherData(self):
        self.dfs = {}                   # Dictionary of Dataframes

        self.fileNames = input("Enter a list of files seperated by 'space': ").split()
        self.columnName = input("Please enter the name of the column you are comparing: ").split()

        self.count = len(self.fileNames) # The number of elements in the list

        try:
            # Save the contents of each of the csv files into the dictionary of Dataframes
            for idx in range(self.count):
                print(f"\n{self.fileNames[idx]}")

                self.dfs[f'df{idx+1}'] = pd.read_csv(self.fileNames[idx])
                print(self.dfs[f'df{idx+1}'])
                
        except FileNotFoundError as e:
            print(f"File not found: {e}")

        except Exception:
            print("Some other exception occured...")
        
    # Find the deferences between csv files
    def mergeFiles(self):
        self.merged_df = pd.DataFrame() # Initialize an empty dataframe

        print("\n\nCombined data:")

        # Merge the DataFrames based on the defined columnName
        #   This process only results in data that is shared between each DataFrame
        for i in range(self.count):
            if self.merged_df.empty:
                self.merged_df = self.dfs[f'df{i+1}']
            else:
                self.merged_df = pd.merge(self.merged_df, self.dfs[f'df{i+1}'], on = self.columnName)

        print(self.merged_df)

        newName = input("\nWhat would you like to name the new csv data file? ")

        self.merged_df.to_csv(newName)

    # consolidate duplicate entreis based on the defined atrribute
    #   This function will only work if you have one dataframe in the dfs dictionary.
    def consolidateDuplicates(self):
        # If the dfs dictionary doesn't have only one dataframe; return to caller
        if not len(self.dfs) == 1:
            print("This function can only run if you have excatly one dataframe in your dictionary.")
            print("Please clear your dataframes and enter only one dataframe you would like to preform this operation on.")
            return

        print("Your dataframe is")
        print(self.dfs[f'df1'])
        print(f"\nThe unique column is {self.columnName}")
        ans = input("Would you like to consolidate the dataframe based on this column? [Y or N] ")

        if ans == 'N':
            print("\nClearing and gathering new data...")
            self.clearDFS()

        df = pd.DataFrame(self.dfs[f'df1'])
        colNames = list(df.columns)
        colNames.remove(self.columnName)

        # Group by the column names, excluding the unique column.
        #   Then convert the unique column into a list for each group
        #   Then convert this new list into a comma-separated string
        grouped = df.groupby(colNames)
        self.result = grouped[self.columnName].apply(list).reset_index()
        self.result[self.columnName] = self.result[self.columnName].apply(lambda x: ', '.join(map(str, x)))

        print(f"\nYour new Dataframe is:\n{self.result}")

        # Write the resulting dataframe to a new csv file
        newName = input("\nWhat would you like to name the new csv data file? ")
        self.result.to_csv(newName)

    # create junction tables from the dataframe
    def junctionData(self):
        # If the dfs dictionary doesn't have only one dataframe; return to caller
        if not len(self.dfs) == 1 and not len(self.columnName) > 1:
            print("This function needs only one variable in the dictionary.")
            print("This function needs to have two columns")
            return

        print("Your dataframe is")
        print(self.dfs[f'df1'])
        print(f"\nThe unique column is {self.columnName}")
        ans = input("Would you like to create a joint table? [Y or N] ")

        if ans == 'N':
            print("\nClearing and gathering new data...")
            self.clearDFS()

        # Splits the values in the specified column
        df = pd.DataFrame(self.dfs[f'df1'])
        df[self.columnName[1]] = df[self.columnName[1]].str.split(', ')

        # Create the new dataframe by exploding out values from the two specified columnNames
        juntionDf = pd.DataFrame({self.columnName[0]: df[self.columnName[0]].explode(),
                                               self.columnName[1]: df[self.columnName[1]].explode()})
        
        print(f"\nYour new Dataframe is:\n{juntionDf}")
        
        newName = input("\nWhat would you like to name the new csv data file? ")
        juntionDf.to_csv(newName, index=False)

    # Remove entries that aren't present in both dataframes
    def removeEntries(self):
        df1 = pd.DataFrame(self.dfs[f'df1'])
        df2 = pd.DataFrame(self.dfs[f'df2'])

        # Merge the two dataframes, find rows that are null, then drop those rows
        merged_df = df2.merge(df1, on = self.columnName, how = 'left')
        missing_rows = merged_df[merged_df.isnull().any(axis = 1)]
        cleaned_df2 = df2.drop(missing_rows.index)

        print(cleaned_df2)

        newName = input("\nWhat would you like to name the new csv data file? ")
        cleaned_df2.to_csv(newName, index=False)

    # Clear all the dataframes in the dfs dictionary
    def clearDFS(self):
        pass

mCSV = mergeCSV.instance()
mCSV.removeEntries()

print(f"\nProgrammed by: {PROGRAMMER_NAME}")