for /f "delims=" %%b in ('git describe') do @set gitrev=%%b
for /f "delims=" %%a in ('git rev-parse --verify HEAD') do @set commitish=%%a
python -v upload_release_asset.py Bigpet/rpcs3 rpcs3-%gitrev%-win_x64.zip %gitrev% %commitish%