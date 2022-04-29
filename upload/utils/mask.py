# imports
import fitz
import re
import nltk
nltk.download('punkt')
class Redactor:
   
    # static methods work independent of class object
    @staticmethod
    def get_sensitive_data(lines, sensitive_data):
       
        """ Function to get all the lines """
         
        # email regex
        # EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+)"
        for line in lines:
           
            # matching the regex to each line
            if re.search(sensitive_data, line, re.IGNORECASE):
                search = re.search(sensitive_data, line, re.IGNORECASE)
                 
                # yields creates a generator
                # generator is used to return
                # values in between function iterations
                yield search.group(1)
 
    # constructor
    def __init__(self):
        return 
    def search_for_text(self, lines, search_str):
        """
        Search for the search string within the document lines
        """
        for line in lines:
            # Find all matches within one line
            results = re.findall(search_str, line, re.IGNORECASE)
            # In case multiple matches within one line
            for result in results:
                yield result
 
    def redact_matching_data(page, matched_values):
        """
        Redacts matching values
        """
        matches_found = 0
        # Loop throughout matching values
        for val in matched_values:
            matches_found += 1
            matching_val_area = page.searchFor(val)
            # Redact matching values
            [page.addRedactAnnot(area, text=" ", fill=(0, 0, 0))
            for area in matching_val_area]
        # Apply the redaction
        page.apply_redactions()
        return matches_found
    
    def redaction(self, file, sensitive_data):
       
        """ main redactor code """
         
        # opening the pdf
        doc = fitz.Document(stream=file, filetype='pdf')
         
        # iterating through pages
        for page in doc:
           
            for data in sensitive_data:
                areas = page.search_for(data)
                 
                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]
                 
            # applying the redaction
            page.apply_redactions()
             
        # # saving it to a new pdf
        doc.save('./files/redacted.pdf')
    
    def redact_txt(self, word_list, sensitive_data):
       
        for i in range(len(word_list)):
            for j in range(len(word_list[i])):
                if word_list[i][j] in sensitive_data:
                    word_list[i][j] = '*****'
        
        file = open('/files/redacted.txt', 'w')
        for sentence in word_list:
            file.writelines(sentence)
            file.write('\n')
        file.close()
  