def upload_file():
    if request.method == "POST":
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if "file" not in request.files:
            return "파일이 없습니다!", 400
        
        file = request.files["file"]

        if file.filename == "":
            return "선택된 파일이 없습니다!", 400
        
        if file and allowed_file(file.filename):
            file_sen=False
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            if scan.scan_file(filepath):
                warning_mail.mail_sender(filepath,file)s
                file_sen=True

            # MongoDB에 메타데이터 저장
            metadata = {
                "filename": filename,
                "uploader": session['user_id'],
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sensitive": file_sen,
                "path": filepath
            }
            files_collection.insert_one(metadata)