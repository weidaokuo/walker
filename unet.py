import torch
from torch import nn
import torchvision
# unet原始网络,训练权重是original_weights_20.pth
class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, input):
        return self.conv(input)


class Unet(nn.Module):
    def __init__(self,in_ch,out_ch):
        super(Unet, self).__init__()

        self.conv1 = DoubleConv(in_ch, 64)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d(2)
        self.conv4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d(2)
        self.conv5 = DoubleConv(512, 1024)
        self.up6 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.conv6 = DoubleConv(1024, 512)
        self.up7 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv7 = DoubleConv(512, 256)
        self.up8 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv8 = DoubleConv(256, 128)
        self.up9 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv9 = DoubleConv(128, 64)
        self.conv10 = nn.Conv2d(64, out_ch, 1)

    def forward(self,x):
        c1=self.conv1(x)
        p1=self.pool1(c1)
        c2=self.conv2(p1)
        p2=self.pool2(c2)
        c3=self.conv3(p2)
        p3=self.pool3(c3)
        c4=self.conv4(p3)
        p4=self.pool4(c4)
        c5=self.conv5(p4)
        up_6= self.up6(c5)
        merge6 = torch.cat([up_6, c4], dim=1)
        c6=self.conv6(merge6)
        up_7=self.up7(c6)
        merge7 = torch.cat([up_7, c3], dim=1)
        c7=self.conv7(merge7)
        up_8=self.up8(c7)
        merge8 = torch.cat([up_8, c2], dim=1)
        c8=self.conv8(merge8)
        up_9=self.up9(c8)
        merge9=torch.cat([up_9,c1],dim=1)
        c9=self.conv9(merge9)
        c10=self.conv10(c9)
        out = nn.Sigmoid()(c10)
        return out

# copy网上的unet网络。训练权重是weights_20.pth
# class Decoder(nn.Module):
#   def __init__(self, in_channels, middle_channels, out_channels):
#     super(Decoder, self).__init__()
#     self.up = nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2)
#     self.conv_relu = nn.Sequential(
#         nn.Conv2d(middle_channels, out_channels, kernel_size=3, padding=1),
#         nn.ReLU(inplace=True)
#         )
#   def forward(self, x1, x2):
#     x1 = self.up(x1)
#     x1 = torch.cat((x1, x2), dim=1)
#     x1 = self.conv_relu(x1)
#     return x1
#
# class Unet(nn.Module):
#     def __init__(self, n_class):
#         super().__init__()
#
#         self.base_model = torchvision.models.resnet18(True)
#         self.base_layers = list(self.base_model.children())
#         self.layer1 = nn.Sequential(
#             nn.Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False),
#             self.base_layers[1],
#             self.base_layers[2])
#         self.layer2 = nn.Sequential(*self.base_layers[3:5])
#         self.layer3 = self.base_layers[5]
#         self.layer4 = self.base_layers[6]
#         self.layer5 = self.base_layers[7]
#         self.decode4 = Decoder(512, 256+256, 256)
#         self.decode3 = Decoder(256, 256+128, 256)
#         self.decode2 = Decoder(256, 128+64, 128)
#         self.decode1 = Decoder(128, 64+64, 64)
#         self.decode0 = nn.Sequential(
#             nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
#             nn.Conv2d(64, 32, kernel_size=3, padding=1, bias=False),
#             nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False)
#             )
#         self.conv_last = nn.Conv2d(64, n_class, 1)
#
#     def forward(self, input):
#         e1 = self.layer1(input) # 64,128,128
#         e2 = self.layer2(e1) # 64,64,64
#         e3 = self.layer3(e2) # 128,32,32
#         e4 = self.layer4(e3) # 256,16,16
#         f = self.layer5(e4) # 512,8,8
#         d4 = self.decode4(f, e4) # 256,16,16
#         d3 = self.decode3(d4, e3) # 256,32,32
#         d2 = self.decode2(d3, e2) # 128,64,64
#         d1 = self.decode1(d2, e1) # 64,128,128
#         d0 = self.decode0(d1) # 64,256,256
#         out = self.conv_last(d0) # 1,256,256
#         return out









