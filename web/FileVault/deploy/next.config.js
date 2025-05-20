module.exports = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/file-access/:id/:file*',
        destination: '/api/files/:id/:file*',
      },
    ];
  }
} 