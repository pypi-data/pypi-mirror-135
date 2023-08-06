import torch
import torch.nn as nn
from einops import rearrange
from util import STFT


class Residual(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(Residual, self).__init__()
        if in_channels != out_channels:
            stride = 2
            self.residual = nn.Sequential(
                nn.Conv2d(
                    in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
                nn.ReLU())
        else:
            stride = 1
            self.residual = nn.Sequential()

        if in_channels != out_channels:
            self.conv1 = nn.Conv2d(
                in_channels, out_channels, kernel_size=(1, 9), stride=stride, padding=(0, 4), bias=False)
        else:
            self.conv1 = nn.Conv2d(
                in_channels, out_channels, kernel_size=(1, 9), stride=stride, padding=(0, 4), bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=(1, 9), stride=1, padding=(0, 4), bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, inputs):
        out = self.conv1(inputs)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        res = self.residual(inputs)
        out = self.relu(out + res)
        return out


class TCResNet(nn.Module):
    def __init__(self, bins, n_channels, n_class):
        super(TCResNet, self).__init__()
        """
        Args:
            bin: frequency bin or feature bin
        """
        self.conv = nn.Conv2d(bins, n_channels[0], kernel_size=(1, 3), padding=(0, 1), bias=False)

        layers = []
        for in_channels, out_channels in zip(n_channels[0:-1], n_channels[1:]):
            layers.append(Residual(in_channels, out_channels))
        self.layers = nn.Sequential(*layers)

        self.pool = nn.AdaptiveAvgPool2d(1)
        self.linear = nn.Linear(n_channels[-1], n_class)

    def forward(self, inputs):
        """
        Args:
            input
            [B, 1, H, W] ~ [B, 1, freq, time]
            reshape -> [B, freq, 1, time]
        """
        B, C, H, W = inputs.shape
        inputs = rearrange(inputs, "b c f t -> b f c t", c=C, f=H)
        out = self.conv(inputs)
        out = self.layers(out)

        out = self.pool(out)
        out = out.view(out.shape[0], -1)
        out = self.linear(out)
        return out


class STFT_TCResnet(nn.Module):
    def __init__(self, filter_length, hop_length, bins, channels, channel_scale, num_classes):
        super(STFT_TCResnet, self).__init__()
        sampling_rate = 16000
        self.filter_length = filter_length
        self.hop_length = hop_length
        self.bins = bins
        self.channels = channels
        self.channel_scale = channel_scale
        self.num_classes = num_classes

        self.stft_layer = STFT(self.filter_length, self.hop_length)
        self.tc_resnet = TCResNet(self.bins, [int(cha * self.channel_scale) for cha in self.channels], self.num_classes)

    def __spectrogram__(self, real, imag):
        spectrogram = torch.sqrt(real ** 2 + imag ** 2)
        return spectrogram

    def forward(self, waveform):
        real, imag = self.stft_layer(waveform)
        spectrogram = self.__spectrogram__(real, imag)
        logits = self.tc_resnet(spectrogram)
        return logits
