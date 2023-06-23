import os
import shutil
from bs4 import BeautifulSoup

# Open the 3D-Movies.html file
with open('3D-Movies.html', 'r') as file:
    # Read the contents of the file
    contents = file.read()

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(contents, 'html.parser')

    # Find all the buttons with the class "button"
    buttons = soup.find_all('button', class_='button')

    # Additional files to copy
    # Additional files to copy
    additional_files = ['styles.css', 'script.js']

    # Create a folder called "MoviesStreamer" in the home directory
    home_dir = os.path.expanduser("~")
    folder_name = os.path.join(home_dir, '3D-MoviesStreamer')
    os.makedirs(folder_name, exist_ok=True)

    print('Copying files...')
    copied_files = []

    # Copy the 3D-Movies.html file to the MoviesStreamer folder
    shutil.copy2('3D-Movies.html', folder_name)
    copied_files.append('3D-Movies.html')

    # Loop through the buttons
    for button in buttons:
        # Get the onclick attribute value
        onclick_value = button.get('onclick')

        # Extract the URL from the onclick attribute value
        url = onclick_value.split("'")[1] if len(onclick_value.split("'")) >= 2 else None

        if url is None:
            # Skip the button if the URL is not found
            print(f"Skipping button (URL not found): {button.text}")
            button.extract()
            continue

        # Check if the file exists
        if os.path.exists(url):
            # Copy the file to the MoviesStreamer folder
            shutil.copy2(url, folder_name)
            copied_files.append(url)
        else:
            # Skip the file and remove the button from 3D-Movies.html
            print(f"Skipping file '{url}' (file not found).")
            button.extract()

    # Copy additional files to the MoviesStreamer folder
    for file in additional_files:
        if os.path.exists(file):
            shutil.copy2(file, folder_name)
            copied_files.append(file)
        else:
            print(f"Skipping file '{file}' (file not found).")

    # Rename the copied 3D-Movies.html file to index.html
    old_file_path = os.path.join(folder_name, '3D-Movies.html')
    new_file_path = os.path.join(folder_name, 'index.html')
    os.rename(old_file_path, new_file_path)

    # Update the modified contents in the index.html file
    with open(new_file_path, 'w') as file:
        file.write(str(soup))

    # Update the modified contents in the copied files
    for copied_file in copied_files:
        if copied_file != '3D-Movies.html':
            file_path = os.path.join(folder_name, copied_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    contents = file.read()
                    updated_contents = contents.replace('Movies', '3D-Movies')
                with open(file_path, 'w') as file:
                    file.write(updated_contents)
            else:
                print(f"Skipping file '{file_path}' (file not found).")

    print('Files copied and renamed successfully:')
    for file in copied_files:
        print(file)

print('All files copied and renamed successfully.')

