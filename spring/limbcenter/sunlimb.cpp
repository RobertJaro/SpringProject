#include <string.h>
#include <stdio.h>
#include <iostream>
#include <math.h>
#include "circlefit/mystuff.h"
#include "circlefit/circle.h"
#include "circlefit/data.h"
#include "circlefit/Utilities.cpp"
#include "circlefit/CircleFitByTaubin.cpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"


#define NumDots 64

using namespace cv;

void raphLimbFit(cv::Mat matImage, Data *dat, int numDots)
{
    cv::Mat matSlice1, matSlice2;
    cv::Mat matSlice11, matSlice22;

    cv::Mat gradXLeft, gradXRight, gradYBottom, gradYTop;
    cv::Point minLoc, maxLoc;
    double minVal, maxVal;

    int naxis1 = matImage.cols;
    int naxis2 = matImage.rows;

    /// Kernels for image gradients.
    /// Over x-axis, forward (from left edge) and backward (from right-edge) direction
    cv::Mat kernelXLeft = (cv::Mat_<float>(1,3)<<-0.5, 0, 0.5);
    cv::Mat kernelXRight = (cv::Mat_<float>(1,3)<<0.5, 0, -0.5);
    /// Over y-axis, forward and backward direction
    cv::Mat kernelYBottom = (cv::Mat_<float>(3,1)<<-0.5, 0, 0.5);
    cv::Mat kernelYTop = (cv::Mat_<float>(3,1)<<0.5, 0, -0.5);

    for (int ii = 0; ii < numDots; ii++)
      {
      int Y = naxis2/4 + ii*naxis2/(2*numDots);
      /// Left-hand slices (no copy)
      matSlice1 = matImage(cv::Range(Y, Y+1), cv::Range(0, naxis1/4));
      cv::blur(matSlice1, matSlice2, cv::Size(7, 7));
      cv::filter2D(matSlice2, gradXLeft, -1, kernelXLeft, cv::Point(-1, -1), 0, cv::BORDER_REPLICATE);
      cv::minMaxLoc(gradXLeft, &minVal, &maxVal, &minLoc, &maxLoc);
      dat->X[ii] = maxLoc.x;
      dat->Y[ii] = Y;
      /// Right-hand slices (no copy)
      matSlice1 = matImage(cv::Range(Y, Y+1), cv::Range(3*naxis1/4, naxis1));
      cv::blur(matSlice1, matSlice2, cv::Size(7, 7));
      cv::filter2D(matSlice2, gradXRight, -1, kernelXRight, cv::Point(-1, -1), 0, cv::BORDER_REPLICATE);
      cv::minMaxLoc(gradXRight, &minVal, &maxVal, &minLoc, &maxLoc);
      dat->X[ii + numDots] = maxLoc.x + 3*naxis1/4;
      dat->Y[ii + numDots] = Y;
      }
    for (int ii1 = 0; ii1 < numDots; ii1++)
      {
      int X = naxis1/4 + ii1*naxis1/(2*numDots);
      ///Bottom slices (no copy)
      matSlice11 = matImage(cv::Range(0, naxis2/4), cv::Range(X, X+1));
      cv::blur(matSlice11, matSlice22, cv::Size(7, 7));
      cv::filter2D(matSlice22, gradYBottom, -1, kernelYBottom, cv::Point(-1, -1), 0, cv::BORDER_REPLICATE);
      cv::minMaxLoc(gradYBottom, &minVal, &maxVal, &minLoc, &maxLoc);
      dat->X[ii1 + 2*numDots] = X;
      dat->Y[ii1 + 2*numDots] = maxLoc.y;
      ///Top slices (no copy)
      matSlice11 = matImage(cv::Range(3*naxis2/4, naxis2), cv::Range(X, X+1));
      cv::blur(matSlice11, matSlice22, cv::Size(7, 7));
      cv::filter2D(matSlice22, gradYTop, -1, kernelYTop, cv::Point(-1, -1), 0, cv::BORDER_REPLICATE);
      cv::minMaxLoc(gradYTop, &minVal, &maxVal, &minLoc, &maxLoc);
      dat->X[ii1 + 3*numDots] = X;
      dat->Y[ii1 + 3*numDots] = maxLoc.y + 3*naxis2/4;
      }
}


Circle getSun(cv::Mat matImage){
   /* calculate sun center, sun radius and RMSE of the radius
      returns: sun.a (X-pos), sun.b (Y-pos), sun.r (radius), sun.s (RMSE) */
   Data dat = Data(NumDots*4);
   Data dat2 = Data(NumDots*4);
   Circle sun;
   int i, ii,n;
   float f;
   n = NumDots;
   raphLimbFit(matImage, &dat, NumDots);
   sun = CircleFitByTaubin(dat);
   if ((sun.s > 2.0) && isnormal(sun.s) && (n > 5)) { /* if error too high, points which don't fit are removed */
      i = 0;
      for (ii=0;ii<dat.n;ii++){
         f = sqrt(powf(dat.X[ii]-sun.a,2)+powf(dat.Y[ii]-sun.b,2));
         if (f<(sun.r+30.0) && f>(sun.r-30.0)) {
            dat2.X[ii-i] = dat.X[ii];
            dat2.Y[ii-i] = dat.Y[ii];
            }
         else {i++;}}
      dat2.n = dat2.n - i;
      dat.n = dat.n - i;
      n = dat.n;
      if (n > 5)
         {
         sun = CircleFitByTaubin(dat2);}
      }
   if ((sun.s > 2.0) && isnormal(sun.s) && (n > 5)) { /* if error too high, points which don't fit are removed */
      i = 0;
      for (ii=0;ii<dat2.n;ii++){
         f = sqrt(powf(dat2.X[ii]-sun.a,2)+powf(dat2.Y[ii]-sun.b,2));
         if (f<sun.r+10.0 && f>sun.r-10.0) {
            dat.X[ii-i] = dat2.X[ii];
            dat.Y[ii-i] = dat2.Y[ii];}
         else {i++;}}
      dat2.n = dat2.n - i;
      dat.n = dat.n - i;
      n = dat.n;
      if (n > 5)
         {sun = CircleFitByTaubin(dat);}
      }
   if ((sun.s > 2.0) && !isnan(sun.s) && (n > 5)) { /* if error too high, points which don't fit are removed */
      i = 0;
      for (ii=0;ii<dat.n;ii++){
         f = sqrt(powf(dat.X[ii]-sun.a,2)+powf(dat.Y[ii]-sun.b,2));
         if (f<sun.r+5.0 && f>sun.r-5.0) {
            dat2.X[ii-i] = dat.X[ii];
            dat2.Y[ii-i] = dat.Y[ii];}
         else {i++;}}
      dat2.n = dat2.n - i;
      dat.n = dat.n - i;
      n = dat.n;
      if (n > 5)
         {sun = CircleFitByTaubin(dat2);}
      }
   if (!isnormal(sun.s)){sun.s= 9.99;sun.a= 0;sun.b=0;sun.r=0;}
   return sun;
}





int main(int argc, char *argv[]){
  // gcc sunlimb.cpp -lopencv_core -lopencv_imgproc -lopencv_highgui -lm -lstdc++ -o sunlimb
  cv::Mat img;
  cv::Mat matImage;
  Circle sun;
  img = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
  /* read sun image and store it into opencv matrix ... */
  
  img.convertTo(matImage, CV_32F);
  sun = getSun(matImage);
  cout << sun.a << endl; // "Center x: "
  cout << sun.b << endl; // "Center y: "
  cout << sun.r << endl; // "Radius  : "
  cout << sun.s << endl; // "rms of r: "
  
  }
