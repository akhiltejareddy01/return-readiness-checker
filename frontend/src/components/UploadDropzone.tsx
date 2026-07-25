import { useRef, useState } from "react";
import type { DragEvent } from "react";

interface Props {
  onAnalyze: (files: File[]) => void;
  loading: boolean;
}

export default function UploadDropzone({ onAnalyze, loading }: Props) {
  const [stagedFiles, setStagedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function addFiles(fileList: FileList | null) {
    if (!fileList) return;
    setStagedFiles((prev) => [...prev, ...Array.from(fileList)]);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    addFiles(e.dataTransfer.files);
  }

  function removeFile(index: number) {
    setStagedFiles((prev) => prev.filter((_, i) => i !== index));
  }

  return (
    <section className="panel">
      <h2>Client Documents</h2>
      <div
        className={`dropzone${isDragging ? " dropzone-active" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <p>Drag &amp; drop client documents here, or click to browse</p>
        <input
          ref={inputRef}
          type="file"
          multiple
          hidden
          onChange={(e) => addFiles(e.target.files)}
        />
      </div>

      {stagedFiles.length > 0 && (
        <ul className="staged-files">
          {stagedFiles.map((file, i) => (
            <li key={`${file.name}-${i}`}>
              <span>{file.name}</span>
              <button type="button" className="link-button" onClick={() => removeFile(i)}>
                remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <button
        type="button"
        className="primary-button"
        disabled={stagedFiles.length === 0 || loading}
        onClick={() => onAnalyze(stagedFiles)}
      >
        {loading ? "Analyzing…" : `Analyze ${stagedFiles.length || ""} Document${stagedFiles.length === 1 ? "" : "s"}`}
      </button>
    </section>
  );
}
