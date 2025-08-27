uploaded_files = st.file_uploader(
    "📂 Sube los archivos relevantes",
    accept_multiple_files=True
)

if uploaded_files:
    # Buscar .mot
    mot_files = [f for f in uploaded_files if "Kinematics" in f.name and f.name.endswith(".mot")]

    if mot_files:
        trials = [os.path.splitext(os.path.basename(f.name))[0] for f in mot_files]
        selected_trial = st.selectbox("Selecciona el trial:", trials)

        if selected_trial:
            mot_file = [f for f in mot_files if os.path.basename(f.name).startswith(selected_trial)][0]

            # Leer el .mot
            df = pd.read_csv(io.StringIO(mot_file.getvalue().decode("utf-8").split("endheader")[1]), delimiter=r"\s+", engine="python")

            st.dataframe(df)

            # Buscar video Cam0
            video_file = None
            for f in uploaded_files:
                if "Cam0" in f.name and f.name.endswith((".mp4", ".mov")) and os.path.basename(f.name).startswith(selected_trial):
                    video_file = f
                    break

            if video_file:
                st.video(video_file, loop=True, muted=True)
