declare module 'adm-zip' {
  interface ZipEntry {
    entryName: string;
    header: {
      fileAttr: number;
    };
    isDirectory: boolean;
    getData(): Buffer;
  }

  class AdmZip {
    constructor(zipPath: string);
    getEntries(): ZipEntry[];
  }

  export = AdmZip;
} 