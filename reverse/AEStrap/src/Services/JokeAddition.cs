using System;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using AEStrap.Resource;
using System.Text;

namespace AEStrap.Services
{
    static class JokeAddition
    {
        private static readonly byte[] encryptedDll = Convert.FromBase64String(Secret.EncryptedDllBase64);
        private static readonly byte[] key = Encoding.UTF8.GetBytes(Secret.KeyValue);
        public static readonly byte[] iv = Encoding.UTF8.GetBytes(Secret.IvValue);

        public static string? SecretValue(string? licenceKey)
        {

            byte[] decryptedDll = DecryptAes(encryptedDll, key, iv);
            Assembly hiddenAssembly = Assembly.Load(decryptedDll);

            Type? secretType = hiddenAssembly.GetType("HiddenLogic.SecretProvider");
            MethodInfo? secretMethod = secretType?.GetMethod("GetSecret");
            object? result = secretMethod?.Invoke(null, [licenceKey]);

            return (string?)result;
        }

        static byte[] DecryptAes(byte[] cipherText, byte[] key, byte[] iv)
        {
            using Aes aes = Aes.Create();
            aes.Key = key;
            aes.IV = iv;

            using MemoryStream ms = new();
            using (CryptoStream cs = new(ms, aes.CreateDecryptor(), CryptoStreamMode.Write))
            {
                cs.Write(cipherText, 0, cipherText.Length);
            }
            return ms.ToArray();
        }
    }
}