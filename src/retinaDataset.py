class retinaDataset(Dataset):
    def __init__(self, imagepath="../input/diabetic-retinopathy-resized/resized_train_cropped/resized_train_cropped", total=None,transform=my_transform):
        self.df = pd.read_csv("../input/diabetic-retinopathy-resized/trainLabels_cropped.csv")
        
        if (total is not None):
            self.df = self.df[:total]
        
        self.transform = transform
        self.imagepath = imagepath
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        img_path = os.path.join(self.imagepath, self.df.iloc[index].image +".jpeg")
        img = Image.open(img_path)
        
        if(self.transform):
            img = self.transform(img)
        
        return img, torch.tensor(self.df.iloc[index].level)
