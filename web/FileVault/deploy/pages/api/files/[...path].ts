import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { path: filePath } = req.query;
    
    const filePathStr = Array.isArray(filePath) ? filePath.join('/') : filePath;
    
    if (!filePathStr) {
      return res.status(400).json({ error: 'Invalid file path' });
    }
    
    // @ts-ignore
    const fullPath = path.join(process.cwd(), 'public', 'uploads', filePathStr);
    
    if (fs.existsSync(fullPath)) {
      if (fs.lstatSync(fullPath).isSymbolicLink()) {
        const targetPath = fs.readlinkSync(fullPath);
        
        const resolvedPath = path.isAbsolute(targetPath) 
          ? targetPath 
          : path.resolve(path.dirname(fullPath), targetPath);
        
        try {
          const content = fs.readFileSync(resolvedPath, 'utf8');
          res.setHeader('Content-Type', 'text/plain');
          return res.status(200).send(content);
        } catch (fsError) {
          const errorMessage = fsError instanceof Error ? fsError.message : String(fsError);
          
          try {
            const content = execSync(`cat "${resolvedPath}"`).toString();
            res.setHeader('Content-Type', 'text/plain');
            return res.status(200).send(content);
          } catch (catError) {
            const catErrorMessage = catError instanceof Error ? catError.message : String(catError);
            return res.status(500).json({ 
              error: 'Failed to read symlink target',
              message: catErrorMessage 
            });
          }
        }
      }
      
      if (fs.existsSync(`${fullPath}.symlink`)) {
        try {
          const targetPath = fs.readFileSync(fullPath, 'utf8').trim();
          
          if (targetPath.startsWith('/')) {
            try {
              const content = fs.readFileSync(targetPath, 'utf8');
              res.setHeader('Content-Type', 'text/plain');
              return res.status(200).send(content);
            } catch (fsError) {
              const errorMessage = fsError instanceof Error ? fsError.message : String(fsError);
              
              try {
                const content = execSync(`cat "${targetPath}"`).toString();
                res.setHeader('Content-Type', 'text/plain');
                return res.status(200).send(content);
              } catch (catError) {
                const catErrorMessage = catError instanceof Error ? catError.message : String(catError);
                return res.status(500).json({ 
                  error: 'Failed to read symlink target',
                  message: catErrorMessage 
                });
              }
            }
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : String(error);
        }
      }
      
      try {
        const content = fs.readFileSync(fullPath, 'utf8');
        const trimmedContent = content.trim();
        
        if (trimmedContent.startsWith('/protected/') && trimmedContent.length < 256) {
          
          try {
            const targetContent = fs.readFileSync(trimmedContent, 'utf8');
            res.setHeader('Content-Type', 'text/plain');
            return res.status(200).send(targetContent);
          } catch (fsError) {
            
            try {
              const targetContent = execSync(`cat "${trimmedContent}"`).toString();
              res.setHeader('Content-Type', 'text/plain');
              return res.status(200).send(targetContent);
            } catch (catError) {
            }
          }
        }
      } catch (error) {
      }
      
      const fileStream = fs.createReadStream(fullPath);
      return fileStream.pipe(res);
    } else {
      return res.status(404).json({ error: 'File not found' });
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ 
      error: 'Internal server error',
      message: errorMessage 
    });
  }
} 