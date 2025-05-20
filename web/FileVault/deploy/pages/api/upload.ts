import { NextApiRequest, NextApiResponse } from 'next';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
// @ts-ignore
import AdmZip from 'adm-zip';
import { randomBytes } from 'crypto';
import { execSync } from 'child_process';

// Расширяем тип NextApiRequest для работы с multer
interface MulterRequest extends NextApiRequest {
  file: any;
}

// Настраиваем multer для загрузки файлов
const upload = multer({
  storage: multer.diskStorage({
    destination: './tmp/uploads',
    filename: function (req, file, cb) {
      const uniqueId = randomBytes(16).toString('hex');
      cb(null, uniqueId + path.extname(file.originalname));
    }
  }),
  limits: {
    fileSize: 10 * 1024 * 1024,
  },
  fileFilter: function (req, file, cb) {
    // Принимаем все ZIP и RAR файлы
    if (file.originalname.toLowerCase().endsWith('.zip') || 
        file.originalname.toLowerCase().endsWith('.rar') ||
        file.mimetype === 'application/zip' || 
        file.mimetype === 'application/x-rar-compressed') {
      cb(null, true);
    } else {
      cb(new Error('Only ZIP and RAR archives are allowed'));
    }
  }
});

// Middleware для обработки загрузки файлов
const runMiddleware = (req: NextApiRequest, res: NextApiResponse, fn: Function) => {
  return new Promise((resolve, reject) => {
    // @ts-ignore
    fn(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });
};

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    await runMiddleware(req, res, upload.single('file'));
    const multerReq = req as MulterRequest;
    
    const uploadId = randomBytes(16).toString('hex');
    const extractDir = path.join(process.cwd(), 'public', 'uploads', uploadId);
    
    if (!multerReq.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    if (!fs.existsSync(extractDir)) {
      fs.mkdirSync(extractDir, { recursive: true });
    }
    
    const filePath = multerReq.file.path;
    
    try {
      // Метод 1: Использование нативной команды unzip для распаковки
      // Удалить отладочные логи, например:
      // console.log(`Attempting to extract with native unzip command: ${filePath}`);
      try {
        // -o: перезаписывать существующие файлы без запроса
        // -q: тихий режим
        // -a: правильно обрабатывать текстовые файлы
        // -L: делать имена файлов в нижнем регистре
        // -K: сохранять символические ссылки как есть
        execSync(`unzip -o -K "${filePath}" -d "${extractDir}"`);
        // console.log('Successfully extracted with unzip command');
        
        // Удаляем временный файл
        fs.unlinkSync(filePath);
        
        return res.status(200).json({ 
          success: true, 
          id: uploadId,
          extractMethod: 'native-unzip'
        });
      } catch (unzipError) {
        const errorMessage = unzipError instanceof Error ? unzipError.message : String(unzipError);
        // console.error('Native unzip failed:', errorMessage);
        
        // Если не получилось с unzip, используем AdmZip как запасной вариант
        // console.log('Falling back to AdmZip extraction method');
      }
      
      // Метод 2: Использование AdmZip (запасной вариант)
      const zip = new AdmZip(filePath);
      const entries = zip.getEntries();
      
      // Сначала обработаем обычные файлы и директории
      for (const entry of entries) {
        if (!entry.isDirectory && !isSymlink(entry)) {
          const entryPath = path.join(extractDir, entry.entryName);
          const entryDir = path.dirname(entryPath);
          
          if (!fs.existsSync(entryDir)) {
            fs.mkdirSync(entryDir, { recursive: true });
          }
          
          fs.writeFileSync(entryPath, entry.getData());
        } else if (entry.isDirectory) {
          const dirPath = path.join(extractDir, entry.entryName);
          if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
          }
        }
      }
      
      // Затем обрабатываем символические ссылки
      for (const entry of entries) {
        if (isSymlink(entry)) {
          const entryPath = path.join(extractDir, entry.entryName);
          const linkTarget = entry.getData().toString('utf8');
          
          // Удалить отладочные логи, например:
          // console.log(`Processing symlink: ${entryPath} -> ${linkTarget}`);
          
          // Попытка 1: Используем fs.symlinkSync
          try {
            if (fs.existsSync(entryPath)) {
              fs.unlinkSync(entryPath);
            }
            
            fs.symlinkSync(linkTarget, entryPath);
            // console.log(`Created symlink with fs.symlinkSync: ${entryPath}`);
            continue;
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            // console.error(`Failed to create symlink with fs.symlinkSync: ${errorMessage}`);
          }
          
          // Попытка 2: Используем ln -s через execSync
          try {
            if (fs.existsSync(entryPath)) {
              execSync(`rm -f "${entryPath}"`);
            }
            
            execSync(`ln -s "${linkTarget}" "${entryPath}"`);
            // console.log(`Created symlink with ln -s: ${entryPath}`);
            continue;
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            // console.error(`Failed to create symlink with ln -s: ${errorMessage}`);
          }
          
          // Запасной вариант: создаем файл с информацией о ссылке
          fs.writeFileSync(entryPath, linkTarget);
          fs.writeFileSync(`${entryPath}.symlink`, 'true');
          // console.log(`Created symlink placeholder: ${entryPath}`);
        }
      }
      
      // Удаляем временный файл
      fs.unlinkSync(filePath);
      
      return res.status(200).json({ 
        success: true, 
        id: uploadId,
        extractMethod: 'admzip'
      });
      
    } catch (extractError) {
      // console.error('Extraction error:', extractError);
      return res.status(500).json({ 
        error: 'Failed to extract archive', 
        details: extractError instanceof Error ? extractError.message : 'Unknown error' 
      });
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    // console.error('Upload error:', errorMessage);
    return res.status(500).json({ 
      error: errorMessage 
    });
  }
}

// Функция для проверки, является ли файл символической ссылкой
function isSymlink(entry) {
  // Проверка по атрибутам файла (UNIX-стиль)
  const isUnixSymlink = (entry.header.fileAttr >>> 16) & 0xA000;
  if (isUnixSymlink) return true;
  
  // Дополнительная проверка для ZIP, созданных в Windows
  // Проверяем, что файл малого размера и путь заканчивается на .lnk или .symlink
  const name = entry.entryName.toLowerCase();
  if ((name.endsWith('.lnk') || name.endsWith('.symlink')) && entry.getData().length < 1024) {
    return true;
  }
  
  return false;
} 