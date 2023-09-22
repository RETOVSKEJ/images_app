# Run the Project:

1. `git clone https://github.com/RETOVSKEJ/images_app`
2. `cd images_app`
4. `docker compose build`       
5. `docker compose up`    
6. `go to localhost:8000/api/` or any route that you want.

IF ERROR `python: can't open file '/app/manage.py': [Errno 2] No such file or directory`:  Make sure to have endline formatting set to LF instead of CRLF (open entrypoint.sh and you will see it in the bottom right corner in Vscode)



**superuser for testing purposes:** (with Custom Tier added from admin)\
login: `test`\
password: `test`\
**staff user without permissions:** (with Basic Tier)\
login: `someUser`\
password: `tester123`


- _api/_ - **POST** new image && **GET LIST** of user's image
- _api/\<int:id>/link_ - **GET** returns token to a shortlived URL of an image (can be accessed only by an image owner)
- _api/\<str:token>_ - **GET** IMAGE from shortlived URL (can be accessed by anyone with a token)
- _media/\<path:file_path>_ - **GET** Route for images (PROTECTED - only the owners can see their images)


1. go to `/api`
2. add image with POST request to `api/`
   - file extensions are validated, only JPEG and PNG are allowed
3. view an image or a thumbnail by clicking on the appriopriate returned link
4. If you're a Enterprise user, go to `api/<image_id>/link` or `api/<image_id>/link?duration=15000` and generate an expiring URL for your image, which can be accessed by everyone with the token.
5. access image from expiring URL by going to `api/<pass_token_here>`



-Staff users gets Enterprise Tier by default, Normal users gets Basic Tier.\
-Maximum custom `ThumbnailSize` height is 1000\
-Maximum size of an Image is 5MB.\
-Shortlived URLs are stored in Redis instead of SQLite -`duration` of URL is 3000 by default, if not given any. if the given `duration` searchParam is either too long (above 30000 seconds) or too short (below 300 seconds), then, the 400 bad request is returned\
-In real-world app, I would definitely use S3 or some other cloud bucket for storing the images. Here, I did everything within Django webserver

### IMPORTANT!
- use `http://localhost:8000/` instead of `http://127.0.0.1:8000/` for docker
