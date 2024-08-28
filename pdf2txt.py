import os
import logging
from pdfminer.high_level import extract_text
from pdfminer.pdftypes import PDFException

# Configure logging
logging.basicConfig(
    filename='pdf_conversion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def convert_pdfs_to_txt(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through all the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            
            try:
                # Extract text from the PDF
                text = extract_text(pdf_path)
                
                # Create a corresponding txt file name
                txt_filename = f"{os.path.splitext(filename)[0]}.txt"
                txt_path = os.path.join(output_folder, txt_filename)
                
                # Write the extracted text to a txt file
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
                
                # Log and print progress
                log_msg = f"Converted: {filename} -> {txt_filename}"
                logging.info(log_msg)
                print(log_msg)

            except PDFException as e:
                # Log and print errors related to PDF processing
                error_msg = f"Failed to convert {filename}: {e}"
                logging.error(error_msg)
                print(error_msg)
            except Exception as e:
                # Log and print any other unforeseen errors
                unexpected_error_msg = f"An unexpected error occurred with {filename}: {e}"
                logging.error(unexpected_error_msg)
                print(unexpected_error_msg)

if __name__ == "__main__":
    input_folder = "tig_corpus (pdf)"
    output_folder = "tig_corpus (txt)"
    
    convert_pdfs_to_txt(input_folder, output_folder)
