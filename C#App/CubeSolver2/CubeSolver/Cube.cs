using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;


namespace CSharpApp
{
    public enum Face
    {
        Up=0, Left=1, Front=2, Right=3, Back=4, Down=5
    }
    public enum Color
    {
        White=0 , Red=1, Blue=2, Orange=3, Green=4, Yellow=5  
    }

    /// <summary>
    /// Data structure representing an NxNxN Rubik's Cube.
    /// </summary>
    public class Cube : IDeepCloneable<Cube>
    {
        public static readonly char[] FaceLetters = {'U', 'L', 'F', 'R', 'B', 'D'};
        public const int FaceCount = 6;
        
        public int Dimension;
        public Color[,] Up, Left, Front, Right, Back, Down; // Individual Face Arrays
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
            Up = Tiles[0];
            Left = Tiles[1];
            Front = Tiles[2];
            Right = Tiles[3];
            Back = Tiles[4];
            Down = Tiles[5];
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
            Up = Tiles[0];
            Left = Tiles[1];
            Front = Tiles[2];
            Right = Tiles[3];
            Back = Tiles[4];
            Down = Tiles[5];
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
                Console.Error.Write("Error: Offset too large");
                return;
            }

            // Rotate the face if no offset (outer layer)
            if (offset == 0)
            {
                RotateFace(face, clockwise);
            }
            
            int offsetInv = Dimension - offset - 1;
            // Cycle pieces to simulate the slice
            switch (face)
            {
                case Face.Down:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Front[offsetInv, i];
                            Front[offsetInv, i] = Left[offsetInv, i];
                            Left[offsetInv, i] = Back[offsetInv, i];
                            Back[offsetInv, i] = Right[offsetInv, i];
                            Right[offsetInv, i] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Front[offsetInv, i];
                            Front[offsetInv, i] = Right[offsetInv, i];
                            Right[offsetInv, i] = Back[offsetInv, i];
                            Back[offsetInv, i] = Left[offsetInv, i];
                            Left[offsetInv, i] = temp;
                        }
                    }
                    break;
                
                case Face.Front:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[offset, i];
                            Down[offset, i] = Right[Dimension - i - 1, offset];
                            Right[Dimension - i - 1, offset] = Up[offsetInv, Dimension - i - 1];
                            Up[offsetInv, Dimension - i - 1] = Left[i, offsetInv];
                            Left[i, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[offset, i];
                            Down[offset, i] = Left[i, offsetInv];
                            Left[i, offsetInv] = Up[offsetInv, Dimension - i - 1];
                            Up[offsetInv, Dimension - i - 1] = Right[Dimension - i - 1, offset];
                            Right[Dimension - i - 1, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Right:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[i, offsetInv];
                            Down[i, offsetInv] = Back[Dimension - i - 1, offset];
                            Back[Dimension - i - 1, offset] = Up[i, offsetInv];
                            Up[i, offsetInv] = Front[i, offsetInv];
                            Front[i, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[i, offsetInv];
                            Down[i, offsetInv] = Front[i, offsetInv];
                            Front[i, offsetInv] = Up[i, offsetInv];
                            Up[i, offsetInv] = Back[Dimension - i - 1, offset];
                            Back[Dimension - i - 1, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Back:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[offsetInv, i];
                            Down[offsetInv, i] = Left[i, offset];
                            Left[i, offset] = Up[offset, Dimension - i - 1];
                            Up[offset, Dimension - i - 1] = Right[Dimension - i - 1, offsetInv];
                            Right[Dimension - i - 1, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[offsetInv, i];
                            Down[offsetInv, i] = Right[Dimension - i - 1, offsetInv];
                            Right[Dimension - i - 1, offsetInv] = Up[offset, Dimension - i - 1];
                            Up[offset, Dimension - i - 1] = Left[i, offset];
                            Left[i, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Left:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[i, offset];
                            Down[i, offset] = Front[i, offset];
                            Front[i, offset] = Up[i, offset];
                            Up[i, offset] = Back[Dimension - i - 1, offsetInv];
                            Back[Dimension - i - 1, offsetInv] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Down[i, offset];
                            Down[i, offset] = Back[Dimension - i - 1, offsetInv];
                            Back[Dimension - i - 1, offsetInv] = Up[i, offset];
                            Up[i, offset] = Front[i, offset];
                            Front[i, offset] = temp;
                        }
                    }
                    break;
                
                case Face.Up:
                    if (clockwise)
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Front[offset, i];
                            Front[offset, i] = Right[offset, i];
                            Right[offset, i] = Back[offset, i];
                            Back[offset, i] = Left[offset, i];
                            Left[offset, i] = temp;
                        }
                    }
                    else
                    {
                        for (int i = 0; i < Dimension; ++i)
                        {
                            var temp = Front[offset, i];
                            Front[offset, i] = Left[offset, i];
                            Left[offset, i] = Back[offset, i];
                            Back[offset, i] = Right[offset, i];
                            Right[offset, i] = temp;
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