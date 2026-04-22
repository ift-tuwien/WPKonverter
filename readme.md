# Usage

## Preparation

1. Open Outlook Classic
2. Move WPK mails into folder e.g. one named “WPK”
3. Click on “Datei”
4. Click on “Öffnen und Exportieren”
5. Click on “Importieren/Exportieren”

   ![Importieren/Exportieren](doc/pictures/export.webp)

6. Click on “In Datei exportieren” and “Weiter”

   ![In Datei exportieren](doc/pictures/export-to-file.webp)

7. Click on “Durch Trennzeichen getrennte Werte” and “Weiter”

   ![Durch Trennzeichen getrennte Werte](doc/pictures/separated-values.webp)

8. Click on “Durch Trennzeichen getrennte Werte” and “Weiter”

   ![Durch Trennzeichen getrennte Werte](doc/pictures/separated-values.webp)

9. Select the folder from step 2 (e.g. “WPK”) and click on “Weiter”

   ![Folder Selection](doc/pictures/folder-selection.webp)

10. Choose the folder (e.g. `Downloads`) and the filename (e.g. `WPK.CSV`) for the exported file and click on “Weiter”

    ![Save Dialog](doc/pictures/save.webp)

11. Click on “Fertig stellen” to store the file

    ![Fertig stellen](doc/pictures/done.webp)

## Conversion

1. Open “Windows Terminal”
2. Execute the following command

   ```sh
   wpkonverter ~/Donwloads/WKP.CSV
   ```

   Note: The command above assumes that you stored the CSV file from Outlook in a file called `WPK.CSV` in the `Downloads` folder of the current user
