import argparse
import os
from PIL import Image
import torch
import torch.nn as nn

from SemanticHumanMatting.model.model import HumanMatting
from SemanticHumanMatting import inference

def main():
    # --------------- Arguments ---------------
    parser = argparse.ArgumentParser(description='Test Images')
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--pretrained_weight', type=str, required=True)

    args = parser.parse_args()

    if not os.path.exists(args.pretrained_weight):
        print('Cannot find the pretrained model: {0}'.format(args.pretrained_weight))
        exit()

    # --------------- Main ---------------
    # Load Model
    model = HumanMatting(backbone='resnet50')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == 'cuda':
        model = nn.DataParallel(model).cuda().eval()
        model.load_state_dict(torch.load(args.pretrained_weight, weights_only=False))
    else:
        state_dict = torch.load(args.pretrained_weight, map_location="cpu")
        from collections import OrderedDict
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:]
            new_state_dict[name] = v
        model.load_state_dict(new_state_dict)
    model.eval()
    print("Load checkpoint successfully ...")

    # Load Images
    image_path = args.input

    # Process
    image_name = image_path[image_path.rfind('/')+1:image_path.rfind('.')]

    with Image.open(image_path) as img:
        img = img.convert("RGB")

    # inference
    pred_alpha, pred_mask = inference.single_inference(model, img, device=device)

    # save results
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = output_dir + '/' + image_name + '_mesh' + '.png'
    Image.fromarray(((pred_alpha * 255).astype('uint8')), mode='L').save(save_path)

if __name__ == '__main__':
    main()
