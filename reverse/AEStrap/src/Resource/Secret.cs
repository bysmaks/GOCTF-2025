using System;
using System.Net.NetworkInformation;

namespace AEStrap.Resource
{
    class Secret
    {
        public static string EncryptedDllBase64 = "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";
        private readonly static int[] prKey = { 6, 14, 8, 1, 2, 4, 0, 3, 15, 12, 13, 5, 9, 11, 10, 7 };
        private readonly static int[] prIv= { 15, 14, 12, 7, 5, 2, 13, 6, 11, 9, 10, 8, 3, 4, 0, 1 };

        private static string _keyValue = "e2rocfgt347S39tc"; // scrambled version
        public static string KeyValue
        {
            get
            {
                return Decrypt(_keyValue, prKey); // decrypt when accessed
            }
            set
            {
                _keyValue = value;
            }
        }

        private static string _ivValue = "lu8a86hl141c17hx"; // scrambled version
        public static string IvValue
        {
            get
            {
                return Decrypt(_ivValue, prIv); // decrypt when accessed
            }
            set
            {
                _ivValue = value;
            }
        }


        public static string Decrypt(string input, int[] pr)
        {
            char[] result = new char[input.Length];
            for (int i = 0; i < input.Length; i++)
            {
                result[pr[i]] = input[i];
            }
            return new string(result);
        }
    }
}