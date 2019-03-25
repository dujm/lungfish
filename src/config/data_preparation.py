# a function to split a dataframe into train, validation, test
def split_df(df,image_path_col,target_col,val_size,test_size, random_state):
    X = df[image_path_col]
    y= df[target_col]

    from sklearn.model_selection import train_test_split

    X_train, X_val_test, y_train, y_val_test = train_test_split(X, y,
                                                                stratify=y,
                                                                test_size=float(val_size+test_size),random_state=int(random_state))

    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test,
                                                stratify=y_val_test,
                                                test_size=float(test_size)/float(val_size+test_size),random_state=int(random_state))

    print( 'Train dataset (X_train y_train):',y_train.count())
    print('Validataion dataset(X_val, y_val):',y_val.count())
    print('Test dataset (X_test, y_test):',y_test.count())

    return X_train, y_train, X_val, y_val, X_test, y_test



# a function to split images in train, validation directory
def X_split_image(X,source_DIR,dst_DIR):
    import pandas as pd
    import os

    '''
    type(X): dataframe series
    '''

    # create a sample image_path file
    df = pd.DataFrame()
    df['image_path']=X.astype(str)

    # Optional: write df into a csv file
    csv_name = str(dst_DIR)+'_image_path.csv'
    df.to_csv(csv_name,index=False)
    print(df.shape[0],'images are splitted in',dst_DIR)


    # use .strip() to remove trailing whitespace and line breaks
    names= df['image_path'].tolist()

    for filename in os.listdir(source_DIR):
        for name in names:
        # no need for re.search, just use the "in" operator
            if filename in name:
                 shutil.move(os.path.join(source_DIR,filename), dst_DIR)
             # move the file
                 break


# a function to copy images from source_DIR to destination directory
def X_copy_image(X,source_DIR,dst_DIR):
    '''
    type(X): dataframe series
    '''

    import pandas as pd
    import os

    # create a sample image_path file
    df = pd.DataFrame()
    df['image_path']=X.astype(str)
    #merge with df_target_path
    csv_name = str(dst_DIR)+'_image_path.csv'

    df.to_csv(csv_name,index=False)
    print(csv_name,'is created; images are copied in',dst_DIR)


    # use .strip() to remove trailing whitespace and line breaks
    names= df['image_path'].tolist()
    #print(names)

    for filename in os.listdir(source_DIR):
        for name in names:
        # no need for re.search, just use the "in" operator
            if filename in name:
             # move the file
                shutil.copy(os.path.join(source_DIR,filename), dst_DIR)
                break
