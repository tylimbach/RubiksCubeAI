using System;
using System.Data;
using System.Linq;
using System.Runtime.ExceptionServices;
using System.Text.RegularExpressions;

namespace CSharpApp
{
    /// <summary>
    /// I/O class for receiving user input and displaying output via console.
    /// </summary>
    public class MenuLoop
    {
        private Cube _cube = null!;

        /// <summary>
        /// Start the menu loop. Continues until program termination, either by interrupt or user entering "Q".
        /// </summary>
        public void Start()
        {
            Console.Write("Enter a cube dimension: ");
            var input = Console.ReadLine();
            _cube = new Cube(Convert.ToInt32(input));

            while (input != "Q") 
            {
                _cube.Print2D();
                
                Console.Write("Enter a command: ");
                input = Console.ReadLine();

                // Scramble the cube
                if (input == "S")
                {
                    string sequence = _cube.Scramble();
                    Console.WriteLine(sequence);
                    continue;
                }

                // Create new solved cube
                if (input == "N")
                {
                    Console.Write("Enter a cube dimension: ");
                    input = Console.ReadLine();
                    _cube = new Cube(Convert.ToInt32(input));
                    continue;
                }

                // Clear Console
                if (input == "C")
                {
                    Console.Clear();
                    continue;
                }
                
                string[] parsedInput = input.Split(' ');
                string command = parsedInput[0];

                // determine if clockwise or ccw
                bool clockwise = !command.EndsWith("'");
                bool halfTurn = command.EndsWith("2");

                Face face;
                int offset;

                // determine if slice turn and the offset layer
                int idx = 0; // used to increment current character index
                bool slice = char.IsNumber(command[0]);
                if (slice)
                {
                    string offsetString = "";
                    while (char.IsDigit(command[idx]))
                    {
                        offsetString += command[idx];
                        ++idx;
                    }
                    offset = Int32.Parse(offsetString) - 1;
                }
                else
                {
                    offset = 0;
                }

                // Determine which character represents the face
                char faceChar = command[idx];

                // Determine which face to turn
                switch(faceChar) 
                {
                    case 'D':
                        face = Face.Down;
                        break;
                    case 'F':
                        face = Face.Front;
                        break;
                    case 'R':
                        face = Face.Right;
                        break;
                    case 'U':
                        face = Face.Up;
                        break;
                    case 'B':
                        face = Face.Back;
                        break;
                    case 'L':
                        face = Face.Left;
                        break;
                    default:
                        continue;
                }
                
                _cube.Turn(face, clockwise, offset);
                // turn again if half turn (180 degrees)
                if (halfTurn) _cube.Turn(face, clockwise, offset);
            }
        }
    }
}