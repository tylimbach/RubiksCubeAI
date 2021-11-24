// See https://aka.ms/new-console-template for more information

using System;

namespace CSharpApp
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var menu = new MenuLoop();
            menu.Start();
        }
    }
}