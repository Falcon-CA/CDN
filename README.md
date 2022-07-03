# CDN
Access the CDN [here](https://cdn.falconca.ca)

## The CDN itself
I guess this project really isn't a content delivery NETWORK but more a single server delivery system.
It would be better suited with the name of a file server but it's already been branded a CDN and no
point in changing it.

I could have just used apache like I see in most other file servers, but I think it's more fun to create
my own.

## Accessing files and directories
Files and directories can be accessed at `https://cdn.falconca.ca/directory/[id]` and `https://cdn.falconca.ca/file/[id]/[name]`
respectively. A GET request will provide you with the information and full contents of the file/directory,
whereas a HEAD request will provide you with just the information of the file/directory in the headers.

When accessing a directory, you can provide a `mode` argument in the URL options which determines the
format of the content list.
 - normal/no option: Basic HTML UI content
 - csv: CSV text content
 - json: JSON text content

## Making changes to the CDN
Anything to do with editing files or directories within this project has to be done through the API.
The API consists of a few operations to do specific things, but first you need a token (Go ask whoever
is running it to give you one).

Each API operation is run with `https://cdn.falconca.ca/api?operation=[operation]`

### List of operations
 - **create_file**: POST
   - FCA-Name: Form data for the file name
   - FCA-Directory: Form data for where to place the file (empty for root)
   - FCA-Private: Form data (0/1) to see if file should be private
   - FCA-File: File list data for the file to upload
 - **create_directory**: POST
   - FCA-Name: Form data for the directory name
   - FCA-Directory Form data for where to place the directory (empty for root)
   - FCA-Private: Form data (0/1) to see if file should be private
 - **delete_file**: DELETE
   - FCA-File: Form data for the ID of the file to delete
 - **delete_directory**: DELETE
   - FCA-Directory: Form data for the ID of the directory to delete
 - **edit_file**: PUT
   - FCA-FileID: Form data for the ID of the file to edit
   - FCA-Name: Form data for the new name of the file
   - FCA-File: File list data for the new file content
