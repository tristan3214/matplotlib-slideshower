from __future__ import print_function, division, absolute_import

import wx

import AddLinearSpacer as als


def main():
    pass

class Slide(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Slide Show")

        self.display = wx.GetDisplaySize()

        self.image_list = None
        self.current = None # holds currently displayed bitmap
        # stacks that hold the bitmaps
        self.future = []
        self.past = []

        
        self.left = wx.BitmapButton(self, id=101, size=(100,-1), bitmap=wx.ArtProvider.GetBitmap(wx.ART_GO_BACK))
        self.left.Enable(False)
        self.right = wx.BitmapButton(self, id=102, size=(100,-1), bitmap=wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD))
        self.right.Enable(False)
        self.open = wx.BitmapButton(self, id=103, size=(100,-1), bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN))


        png = wx.Image("set001_fit_001_1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = wx.ImageFromBitmap(png)
        image = image.Scale(self.display[0]/1.4, self.display[1]/1.4, wx.IMAGE_QUALITY_HIGH)
        png = wx.BitmapFromImage(image)
        self.img = wx.StaticBitmap(self, -1, size=(self.display[0]/1.4, self.display[1]/1.4))

        
        ## Main sizers
        self.vertSizer = wx.BoxSizer(wx.VERTICAL)

        # sub sizers
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        # place buttons together
        self.buttonSizer.Add(self.left, flag=wx.ALIGN_CENTER)
        als.AddLinearSpacer(self.buttonSizer, 15)
        self.buttonSizer.Add(self.right, flag=wx.ALIGN_CENTER)

        # place arrows and open together
        self.vertSizer.Add(self.img, flag=wx.ALIGN_CENTER)
        self.vertSizer.Add(self.open, flag=wx.ALIGN_CENTER)
        als.AddLinearSpacer(self.vertSizer, 15)
        self.vertSizer.Add(self.buttonSizer, flag=wx.ALIGN_CENTER)
        als.AddLinearSpacer(self.vertSizer, 15)

        self.Bind(wx.EVT_BUTTON, self.onOpen, id=103)
        self.Bind(wx.EVT_BUTTON, self.onLeft, id=101)
        self.Bind(wx.EVT_BUTTON, self.onRight, id=102)
        
        self.SetSizer(self.vertSizer)
        self.vertSizer.Fit(self)

    def onOpen(self, evt):
        print("Opening")
        openFileDialog = wx.FileDialog(self, "Open Image List", "", "", "List (*.ls)|*.ls", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        
        fileName = openFileDialog.GetFilename()

        # put image list in a python list
        image_list = []
        f = open(fileName, 'r')
        for line in f:
            image_list.append(line.rstrip())
        f.close()

        print(image_list)
        # convert every image to wx Image
        png_list = []
        for image in image_list:
            png = wx.Image(image, wx.BITMAP_TYPE_ANY)
            png_list.append(png)

        # store pngs
        print(image_list[::-1])
        png_list = png_list[::-1]
        for png in png_list[:-1]:
            self.future.append(png)

        # display first png
        self.current = png_list[-1] # put into current buffer
        png = self.current.Scale(self.display[0]/1.4, self.display[1]/1.4, wx.IMAGE_QUALITY_HIGH)
        png = wx.BitmapFromImage(png)
        self.img.SetBitmap(png)

        self.Refresh()
        self.right.Enable(True)

    def onLeft(self, evt):
        # put current image into future stack and grab a new current image from past stack
        self.future.append(self.current)
        self.current = self.past.pop()
        
        png = self.current.Scale(self.display[0]/1.4, self.display[1]/1.4, wx.IMAGE_QUALITY_HIGH)
        png = wx.BitmapFromImage(png)
        self.img.SetBitmap(png)
        self.Refresh()
        if len(self.past) <= 0:
            self.left.Enable(False)

        self.right.Enable(True)

    def onRight(self, evt):
        # put current image into past stack and load in a new image from future stack
        self.past.append(self.current)
        self.current = self.future.pop()

        png = self.current.Scale(self.display[0]/1.4, self.display[1]/1.4, wx.IMAGE_QUALITY_HIGH)
        png = wx.BitmapFromImage(png)
        self.img.SetBitmap(png)
        self.Refresh()

        if len(self.future) <= 0:
            self.right.Enable(False)
        self.left.Enable(True)

if __name__ == "__main__":
    app = wx.App(False)
    app.frame = Slide()
    app.frame.Show()

    app.MainLoop()
