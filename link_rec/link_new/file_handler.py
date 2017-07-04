import pickle
from preprocess_text import TextProcessing

############################################################################################
        # General File Handler; Basic Functionality with cleaning of txt files
############################################################################################

# TODO: This doesn't handle cleaning Byte Files or other types of files but should implement soon...

class FileProcessor(object):
    """
    General File Processor with very basic functions
    """
    def __init__(self, filename, type_file):
        """
        Initiate the File Object;
        Parameter:
            -filename: existing file path
        """
        assert type(filename) == str
        try:
            f = open(filename) # checks to see if file exists
            # input('If it is a training file make sure label is last column, press enter to continue...')
            self.file = filename
            self.type = type_file
        except:
            raise Exception('Could not find filename or file path')

    def readFile(self):
        """ Read normal file and return's the lines"""
        f = open(self.file)
        lines = f.readlines()
        f.close()
        return [line for line in lines if line != '\n' and line != None]
        # return lines

    def writeFile(self):
        """ Write to a txt file """
        pass

    def eraseFile(self):
        """ Erase's a normal file """
        with open(self.file, 'w') as f:
            pass

    def readByteFile(self):
        """
        Read any Byte File;
        """
        b = []
        with open(self.file, 'rb') as f:
            while True:
                try:
                    b.append(pickle.load(f))  # think this way should work best
                except EOFError:
                    break
        return [line for line in b if line != '\n' and line != None]

    def writeByteFile(self, line):
        """
        """
        pass

    def eraseByteFile(self):
        """ Erase's a Byte file """
        with open(self.file, 'wb') as f:
            pass

    def cleanFile(self):
        """ Returns content of TXT file in tokenized format without punctuation, stop words, etc """
        # input('This only cleans contents in a TXT type file, press enter to continue...')
        t = TextProcessing()
        data, label = [], []
        if self.type == 'train':
            lines = self.readFile()
            for line in lines:
                line = line.replace('\n', '')
                line = t.tokenize(line)
                raw_data, raw_label = line[:-1], line[-1]
                raw_data = [i.lower() for i in raw_data]
                raw_data = t.remove_punctuation_list(raw_data)
                raw_label = t.remove_punctuation_line(raw_label.lower())
                raw_data = t.remove_stop_words_list(raw_data)
                raw_label = t.remove_stop_words_list(raw_label) # pretty unsure whether i should do this..
                data.append(raw_data)
                label.append(raw_label)
            return data, [y for l in label for y in l]
        elif self.type == 'test':
            lines = self.readFile()
            for line in lines:
                line = line.replace('\n', '')
                line = t.tokenize(line)
                line = t.remove_punctuation_list(line)
                line = t.remove_stop_words_list(line)
                data.append(line)
            return data
        else:
            raise Exception('File should either be train or test...')

# if __name__ == '__main__':
#     t = TextProcessing()
