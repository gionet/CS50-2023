#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //By dividing 3, to not have R + G + B > 255
            int pixel = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            //By making R = G = B = value x. To have gray colour point
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = pixel;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    //iterate through rows
    for (int i = 0; i < height; i++)
    {
        //iterate through columns
        for (int j = 0; j < width; j++)
        {
            float blue = 0, green = 0, red = 0;
            float counter = 0;

            //iterate through the pixels around the current pixel x-axis
            for (int x = -1; x < 2; x++)
            {
                //iterate through the pixels around the current pixel y-axis
                for (int y = -1;  y < 2; y ++)
                {
                    //if its out of bound x-axis
                    if (i + x < 0 || i + x > height - 1)
                    {
                        continue;
                    }
                    //if its out of bound y-axis
                    if (j + y < 0 || j + y > width - 1)
                    {
                        continue;
                    }
                    //Stores the R , G , B value
                    blue += image[i + x][j + y].rgbtBlue;
                    green += image[i + x][j + y].rgbtGreen;
                    red += image[i + x][j + y].rgbtRed;

                    //stores the valid pixel counts
                    counter++;
                }
            }
            //stores the R , G , B value in temporary matrix
            temp[i][j].rgbtBlue = round(blue / counter);
            temp[i][j].rgbtGreen = round(green / counter);
            temp[i][j].rgbtRed = round(red / counter);

            //**Cannot be inside the same loop, as the below means to edit the current pixel which will result in affecting the next pixel calculation.**//
            //image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            //image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            //image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    //iterate through matrix and replace the image pixels from temp value
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gxBlue = 0, gxGreen = 0, gxRed = 0;
            int gyBlue = 0, gyGreen = 0, gyRed = 0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    if (i + x < 0 || i + x > height - 1)
                    {
                        continue;
                    }
                    if (j + y < 0 || j + y > width - 1)
                    {
                        continue;
                    }

                    gxBlue += image[i + x][j + y].rgbtBlue * gx[x + 1][y + 1];
                    gyBlue += image[i + x][j + y].rgbtBlue * gy[x + 1][y + 1];

                    gxGreen += image[i + x][j + y].rgbtGreen * gx[x + 1][y + 1];
                    gyGreen += image[i + x][j + y].rgbtGreen * gy[x + 1][y + 1];

                    gxRed += image[i + x][j + y].rgbtRed * gx[x + 1][y + 1];
                    gyRed += image[i + x][j + y].rgbtRed * gy[x + 1][y + 1];
                }
            }

            int blue = round(sqrt(gxBlue * gxBlue + gyBlue * gyBlue));
            int green = round(sqrt(gxGreen * gxGreen + gyGreen * gyGreen));
            int red = round(sqrt(gxRed * gxRed + gyRed * gyRed));

            temp[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
            temp[i][j].rgbtGreen = (green > 255) ? 255 : green;
            temp[i][j].rgbtRed = (red > 255) ? 255 : red;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }

    }
    return;
}
