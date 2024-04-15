import os
import shutil

def copy_pdf_files(input_dir, output_dir, sheet_number):
    # Get the full path to the input directory within the current working directory
    input_dir = os.path.join(os.getcwd(), input_dir)

    # Get the full path to the output directory within the current working directory
    output_dir = os.path.join(os.getcwd(), output_dir)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        raise Exception(f"Input directory {input_dir} does not exist.")

    copy_counter = 0    
    
    # Iterate through folders in the input directory
    for folder_name in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder_name)
        
        # Check if the item in the input directory is a directory
        if os.path.isdir(folder_path):
            pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.pdf')]
            
            # Check for the number of PDF files in the folder
            if len(pdf_files) == 1:
                # Construct the new PDF file name in the output directory
                new_file_name = f"DiscMath_{sheet_number.replace(' ', '')}_{folder_name.split('_',1)[1]}_marked.pdf"
                new_file_path = os.path.join(output_dir, new_file_name)
                
                # Copy the PDF file from input to output directory
                shutil.copy2(os.path.join(folder_path, pdf_files[0]), new_file_path)
                copy_counter += 1
                #print(f"Copied: {os.path.join(folder_name, pdf_files[0])} to {new_file_name}")
            elif len(pdf_files) > 1:
                print(f"Warning: Folder {folder_name} contains multiple PDF files. Skipping.")
            else:
                print(f"Warning: Folder {folder_name} does not contain any PDF files. Skipping.")
    
    print(f"Successfully copied {copy_counter} PDF files to {output_dir}.")

if __name__ == "__main__":
    sheet_number = input("Current sheet number (eg. 01): ")
    
    input_dir = f"sheet{sheet_number}"  # Replace with your input directory path
    output_dir = f"Korrekturen/sheet{sheet_number}"  # Replace with your output directory path
    sheet_number = f"Sheet{sheet_number}"  # Replace with your sheet number

    copy_pdf_files(input_dir, output_dir, sheet_number)