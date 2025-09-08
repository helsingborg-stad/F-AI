import { writable, type Readable } from 'svelte/store'

export interface FileWithState {
  id: string
  file: File
  state: 'valid' | 'invalid' | 'pending'
  parsedContents: string | null
}

export interface InlineFilesHook {
  files: Readable<FileWithState[]>
  canChangeFiles: Readable<boolean>

  getFileId(file: File): string

  setFiles(newRawFiles: File[]): void

  removeFile(fileId: string): void
}

export function useInlineFiles(): InlineFilesHook {
  let filesInternal: FileWithState[] = []
  const files = writable<FileWithState[]>(filesInternal)
  const canChangeFiles = writable(true)
  let isParsing = false

  function getFileId(file: File) {
    return file.name + file.lastModified
  }

  function updateFileInList(fileWithState: FileWithState) {
    const idx = filesInternal.findIndex((v) => v.id === fileWithState.id)
    if (idx > -1) {
      filesInternal[idx] = fileWithState
    } else {
      filesInternal.push(fileWithState)
    }
    files.set(filesInternal)
  }

  async function parseFile(fileWithState: FileWithState): Promise<string | null> {
    const formData = new FormData()
    formData.append('file', fileWithState.file)

    const response = await fetch('/api/files/parse', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      console.log('parseFile error', await response.text())
      return null
    }

    const json = await response.json()
    console.log('parseFile', json)
    return json.contents
  }

  async function parseFiles(newFiles: File[]): Promise<void> {
    const stateFiles = newFiles.map<FileWithState>((f) => ({
      id: getFileId(f),
      file: f,
      state: 'pending',
      parsedContents: null,
    }))
    filesInternal = stateFiles
    files.set(filesInternal)

    for (const file of stateFiles) {
      const contents = await parseFile(file)
      updateFileInList({
        ...file,
        state: contents !== null ? 'valid' : 'invalid',
        parsedContents: contents,
      })
    }
  }

  return {
    files,
    canChangeFiles,
    getFileId,
    setFiles(newRawFiles: File[]) {
      console.log(
        'setFiles',
        newRawFiles.map((f) => f.name),
      )
      if (isParsing) {
        return
      }

      isParsing = true
      canChangeFiles.set(false)

      parseFiles(newRawFiles).finally(() => {
        isParsing = false
        canChangeFiles.set(true)
      })
    },
    removeFile(fileId: string) {
      console.log('removeFile', fileId)
      const idx = filesInternal.findIndex((v) => v.id === fileId)
      if (idx > -1) {
        filesInternal.splice(idx, 1)
        files.set(filesInternal)
      }
    },
  }
}
