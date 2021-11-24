using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;

namespace CSharpApp
{
    /// <summary>
    /// Enum representing the 6 possible faces of a cube.
    /// </summary>
    public enum Face
    {
        Up=0, Left=1, Front=2, Right=3, Back=4, Down=5
    }
    
    /// <summary>
    /// Enum representing the 6 possible colors of a tile on a cube.
    /// </summary>
    public enum Color
    {
        White=0 , Red=1, Blue=2, Orange=3, Green=4, Yellow=5  
    }
    
    /// <summary>
    /// Data structure representing an NxNxN Rubik's Cube.
    /// </summary>
    public class Cube : IDeepCloneable<Cube>
    {
        // Constants to represent the index for each face
        public const int Up = 0;
        public const int Left = 1;
        public const int Front = 2;
        public const int Right = 3;
        public const int Back = 4;
        public const int Down = 5;
        
        public static readonly char[] FaceLetters = {'U', 'L', 'F', 'R', 'B', 'D'};
        public const int FaceCount = 6;
        
        public int Dimension;
        public Color[][,] Tiles = new Color[FaceCount][,]; // 6 [Dimension x Dimension] arrays to represent faces 

        /// <summary>
        /// Create an uninitialized 3x3x3 Cube.
        /// </summary>
        private Cube()
        {
            for (var i = 0; i < FaceCount; ++i)
            {
                Tiles[i] = new Color[3, 3];
            }
        }
        
        /// <summary>
        /// Create a solved Cube of size NxNxN.
        /// </summary>
        /// <param name="dimension">Integer number of pieces along one edge of the cube, including corners.</param>
        public Cube(int dimension)
        {
            Dimension = dimension;
            for (var i=0; i < FaceCount; ++i)
            {
                Tiles[i] = new Color[Dimension, Dimension];
                for (var j=0; j < dimension; ++j)
                {
                    for (var k=0; k < dimension; ++k)
                    {
                        Tiles[i][j, k] = (Color) i;
                    }
                }
            }
        }

        /// <summary>
        /// Turn one face/slice of the cube 90 degrees.
        /// </summary>
        /// <param name="face">Face to turn. Slice turns with offsets turn inner faces.</param>
        /// <param name="clockwise">Clockwise bool: true if clockwise, false if counterclockwise.</param>
        /// <param name="offset">Integer representing the number of layers away from the outer face.</param>
        public void Turn(Face face, bool clockwise, int offset)
        {
            // Validate Input
            if (offset >= Dimension - 1)
            {
                Console.Error.WriteLine("Error: Offset too large");
                return;
            }

            // Rotate the face if no offset (outer layer)
            if (offset == 0)
            {
                RotateFace(face, clockwise);
            }
            
            // Cycle pieces to simulate the slice
            int offsetInv = Dimension - offset - 1; // Offset from "opposite" face
            switch (face)
            {
                case Face.Down:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Front][offsetInv, i];
                            Tiles[Front][offsetInv, i] = Tiles[Left][offsetInv, i];
                            Tiles[Left][offsetInv, i] = Tiles[Back][offsetInv, i];
                            Tiles[Back][offsetInv, i] = Tiles[Right][offsetInv, i];
                            Tiles[Right][offsetInv, i] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Front][offsetInv, i];
                            Tiles[Front][offsetInv, i] = Tiles[Right][offsetInv, i];
                            Tiles[Right][offsetInv, i] = Tiles[Back][offsetInv, i];
                            Tiles[Back][offsetInv, i] = Tiles[Left][offsetInv, i];
                            Tiles[Left][offsetInv, i] = temp;
                        }
                    }
                    break;
                
                case Face.Front:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][offset, i];
                            Tiles[Down][offset, i] = Tiles[Right][Dimension - i - 1, offset];
                            Tiles[Right][Dimension - i - 1, offset] = Tiles[Up][offsetInv, Dimension - i - 1];
                            Tiles[Up][offsetInv, Dimension - i - 1] = Tiles[Left][i, offsetInv];
                            Tiles[Left][i, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][offset, i];
                            Tiles[Down][offset, i] = Tiles[Left][i, offsetInv];
                            Tiles[Left][i, offsetInv] = Tiles[Up][offsetInv, Dimension - i - 1];
                            Tiles[Up][offsetInv, Dimension - i - 1] = Tiles[Right][Dimension - i - 1, offset];
                            Tiles[Right][Dimension - i - 1, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Right:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][i, offsetInv];
                            Tiles[Down][i, offsetInv] = Tiles[Back][Dimension - i - 1, offset];
                            Tiles[Back][Dimension - i - 1, offset] = Tiles[Up][i, offsetInv];
                            Tiles[Up][i, offsetInv] = Tiles[Front][i, offsetInv];
                            Tiles[Front][i, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][i, offsetInv];
                            Tiles[Down][i, offsetInv] = Tiles[Front][i, offsetInv];
                            Tiles[Front][i, offsetInv] = Tiles[Up][i, offsetInv];
                            Tiles[Up][i, offsetInv] = Tiles[Back][Dimension - i - 1, offset];
                            Tiles[Back][Dimension - i - 1, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Back:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][offsetInv, i];
                            Tiles[Down][offsetInv, i] = Tiles[Left][i, offset];
                            Tiles[Left][i, offset] = Tiles[Up][offset, Dimension - i - 1];
                            Tiles[Up][offset, Dimension - i - 1] = Tiles[Right][Dimension - i - 1, offsetInv];
                            Tiles[Right][Dimension - i - 1, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][offsetInv, i];
                            Tiles[Down][offsetInv, i] = Tiles[Right][Dimension - i - 1, offsetInv];
                            Tiles[Right][Dimension - i - 1, offsetInv] = Tiles[Up][offset, Dimension - i - 1];
                            Tiles[Up][offset, Dimension - i - 1] = Tiles[Left][i, offset];
                            Tiles[Left][i, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Left:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][i, offset];
                            Tiles[Down][i, offset] = Tiles[Front][i, offset];
                            Tiles[Front][i, offset] = Tiles[Up][i, offset];
                            Tiles[Up][i, offset] = Tiles[Back][Dimension - i - 1, offsetInv];
                            Tiles[Back][Dimension - i - 1, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Down][i, offset];
                            Tiles[Down][i, offset] = Tiles[Back][Dimension - i - 1, offsetInv];
                            Tiles[Back][Dimension - i - 1, offsetInv] = Tiles[Up][i, offset];
                            Tiles[Up][i, offset] = Tiles[Front][i, offset];
                            Tiles[Front][i, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Up:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Front][offset, i];
                            Tiles[Front][offset, i] = Tiles[Right][offset, i];
                            Tiles[Right][offset, i] = Tiles[Back][offset, i];
                            Tiles[Back][offset, i] = Tiles[Left][offset, i];
                            Tiles[Left][offset, i] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Tiles[Front][offset, i];
                            Tiles[Front][offset, i] = Tiles[Left][offset, i];
                            Tiles[Left][offset, i] = Tiles[Back][offset, i];
                            Tiles[Back][offset, i] = Tiles[Right][offset, i];
                            Tiles[Right][offset, i] = temp;
                        }
                    }
                    break;
            }
        }

        /// <summary>
        /// Scramble the cube using a generated pseudorandom sequence.
        /// Returns a string representing the sequence used to scramble the cube.
        /// </summary>
        public string Scramble()
        {
            var random = new Random();
            int scrambleLength = (Dimension - 2) * 10 + 20; // length is multiple of cube size
            int offset = 0;

            string sequence = "";
            int previousFaceInt = -1;
            for (int i = 0; i < scrambleLength; ++i)
            {
                // 1/6 chance of half turn
                bool halfTurn = (random.Next(6) == 0);
                // 1/6 chance for each face (prune same face as last move)
                int faceInt = (random.Next(6));
                while (faceInt == previousFaceInt) faceInt = (random.Next(6));
                previousFaceInt = faceInt;

                // Always clockwise if half turn, 1/2 chance otherwise
                bool clockwise = (halfTurn || (random.Next(2) > 0));
                // No offset turns on 3x3 or smaller, otherwise equal chance of offsets from 0 to ((Dimension+1)/2)
                if (Dimension > 3) offset = random.Next((Dimension + 1) / 2);

                // Build the string representing the move in cube notation and append it to sequence
                if (offset > 0) sequence += (offset + 1);
                sequence += FaceLetters[faceInt];
                if (halfTurn) sequence += '2';
                if (!clockwise) sequence += "'";
                sequence += ' ';
                
                // Do the turn
                Turn((Face) faceInt, clockwise, offset);
                if (halfTurn) Turn((Face) faceInt, clockwise, offset); // Same turn twice if half turn
            }
            return sequence;
        }
        
        /// <summary>
        /// Rotate the 2D matrix representing a face by 90 degrees.
        /// </summary>
        /// <param name="face">Face of the cube to rotate.</param>
        /// <param name="clockwise">Clockwise bool: true if clockwise, false if counterclockwise.</param>
        private void RotateFace(Face face, bool clockwise)
        {
            int f = (int)face;
            
            // Construct a copy of the face to rotate
            var result = new Color[Dimension, Dimension];
            for (int j = 0; j < Dimension; ++j)
            {
                for (int k = 0; k < Dimension; ++k)
                {
                    result[j, k] = Tiles[f][j, k];
                }
            }

            // Transpose
            for (int i = 0; i < Dimension; ++i)
            {
                for (int j = 0; j < Dimension; ++j)
                {
                    result[j, i] = Tiles[f][i, j];
                }
            }

            if (clockwise)
            {
                // Reverse Rows
                for (int i = 0; i < Dimension; ++i)
                {
                    for (int j = 0; j < Dimension / 2; ++j)
                    {
                        (result[i, j], result[i, Dimension - j - 1]) = 
                            (result[i, Dimension - j - 1], result[i, j]);
                    }
                }
            }
            else
            {
                // Reverse Columns
                for (int i = 0; i < Dimension; ++i)
                {
                    for (int j = 0; j < Dimension / 2; ++j)
                    {
                        (result[j, i], result[Dimension - j - 1, i]) = 
                            (result[Dimension - j - 1, i], result[j, i]);
                    }
                }
            }

            Tiles[f] = result;
        }

        readonly ConsoleColor[] _consoleColors = {ConsoleColor.White, ConsoleColor.Red, ConsoleColor.Blue, ConsoleColor.Magenta, 
            ConsoleColor.Green, ConsoleColor.Yellow};
        
        /// <summary>
        /// Set the console background color based on
        /// </summary>
        /// <param name="color">Color of the square to display.</param>
        private void PrintColoredSquare(Color color)
        {
            Console.BackgroundColor = _consoleColors[(int) color];
            Console.Write("   ");
            Console.ResetColor();
        }
        
        /// <summary>
        /// Display the unfolded 2D cube in the console.
        /// </summary>
        public void Print2D()
        {
            // Top face
            for (var j=0; j < Dimension; ++j)
            {
                for (int a = 0; a <= Dimension * 4 - 1; a++)
                {
                    Console.Write(" ");
                }
                for (var k=0; k < Dimension; ++k)
                {
                    PrintColoredSquare(Tiles[0][j, k]);
                    Console.Write(" ");
                }
                Console.WriteLine();
            }
            
            // Middle 4 faces
            for (var j=0; j < Dimension; ++j)
            {
                for (var i=1; i < 5; ++i)
                {
                    for (var k=0; k < Dimension; ++k)
                    {
                        PrintColoredSquare(Tiles[i][j, k]);
                        Console.Write(" ");
                    }
                    Console.ResetColor();
                    //Console.Write(" ");
                }
                Console.WriteLine();
            }


            // Bottom face
            for (var j=0; j < Dimension; ++j)
            {
                for (int a = 0; a <= Dimension * 4 - 1; a++)
                {
                    Console.Write(" ");
                }
                for (var k=0; k < Dimension; ++k)
                {
                    PrintColoredSquare(Tiles[5][j, k]);
                    Console.Write(" ");
                }
                Console.ResetColor();
                Console.WriteLine();
            }
            Console.WriteLine();
        }
        
        object IDeepCloneable.DeepClone()
        {
            return DeepClone();
        }
        
        public Cube DeepClone()
        {
            var copiedTiles = new Color[FaceCount][,];
            for (var i=0; i < FaceCount; ++i)
            {
                copiedTiles[i] = new Color[Dimension, Dimension];
                for (var j=0; j < Dimension; ++j)
                {
                    for (var k=0; k < Dimension; ++k)
                    {
                        copiedTiles[i][j, k] = Tiles[i][j, k];
                    }
                }
            }
            var copiedCube = new Cube
            {
                Tiles = copiedTiles,
                Dimension = Dimension
            };
            return copiedCube;
        }
    }
    
    public interface IDeepCloneable
    {
        object DeepClone();
    }
    
    public interface IDeepCloneable<T> : IDeepCloneable
    {
        new T DeepClone();
    }
}