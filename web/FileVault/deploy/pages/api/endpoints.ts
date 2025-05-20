import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const endpoints = {
    "api": {
      "/api/upload": {
        "method": "POST",
        "description": "Upload a file",
        "contentType": "multipart/form-data",
        "formFieldName": "file"
      }
    },
    "pages": {
      "/upload": "Web interface for file uploads",
      "/files/{id}": "View and access uploaded files"
    }
  };

  res.status(200).json(endpoints);
} 