# Azure File Storage FastApi Server

## Description

FastApi Server receives requests and stores files in Azure Blob Storage.  
Metadata about the files is stored in Azure MySql Database.  
The files are encrypted and compressed before storage.  

## Testing

Start server with uvicorn:
```
uvicorn files_storage_app:storageapp --reload
```


1. Upload
```
curl.exe -X 'POST' -F "file=@../../file_name"   'http://127.0.0.1:8000/uploadfile/owner_name/file_name'
```

2. Download
```
curl.exe 'http://127.0.0.1:8000/file/owner_name/file_name'
```

3. Head
```
curl.exe -I -L 'http://127.0.0.1:8000/file/owner_name/file_name'
```
