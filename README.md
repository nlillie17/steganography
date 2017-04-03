# steganography
Functions to encode messages into pictures and decode pictures with messages in them

In terms of computer security, steganography is hiding data within other data. In this case, the container data is an image file (jpg, png, etc.) and the "encrypted" data is text. In 2010, Russia spies were accused of using this same technique for communicating with their agents abroad. 

Steganography has two main components, encoding and decoding. Broadly, encoding is taking an input message, converting it into binary, and then hiding that binary in the RGB pixel values of an image. By changing the lowest order digit of pixels to a 0 or 1, the picture will maintain its appearance to the eye but will have a hidden sequence of bits encoded into it.

I will be using openCV (http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html), a python library, that will do a lot of the image handeling. 

1. Encoding
  a. Using CV, transform picture into a numpy array, where each pixel is represented by it's RGB value
  
  
  
    def steganographize( image_name, message ):
      message = txt_to_str(message)
      raw_image = cv2.imread(image_name,cv2.IMREAD_COLOR) 
      image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)

      new_image = image.copy()
      num_rows, num_cols, num_chans = new_image.shape
      bit_list = []
      bin_digits = []
      new_vals = []

      binary_message = message_to_binary(message)
      print(binary_message)
      vals_to_change = len(binary_message)

      for row in range(num_rows):
          for col in range(num_cols):
              r, g, b = image[row,col]

              ...
  
  
  b. Transform message into binary. The difficult part of transforming a message is that most ASCII characters are represented in 8 bit incriments. However, special characters and punctuation are represented in 6-7 bit incriments. This will make decoding very difficult. So, I pad the ASCII characters with less than 8 bits with 2's to make sure that the decoding only has to handle 8 bit incriments. I used a dictionary, in excel, for the ASCII punctuation to binary conversion (with modification with the pads). For everything else, I just functions ord() and bin(). I convert the ASCII to its character, decimal number and then convert that into binary.(https://github.com/nlillie17/steganography/blob/master/custom_dict.png)
  
  
  
      def message_to_binary (message):
        binary_message = ''

        for i in message:
            binary_message += letter_to_binary(i)
        binary_message += '00000000'

        return binary_message



        def letter_to_binary (letter):
        '''takes in a letter and returns binary, handles some edge cases!'''

        y = check_punctuation(letter)
        if y != None:
            return y

        else:
            num = ord(letter)
            binary = bin(num)
            binary2 =''
            for i in binary:
                if i.isdigit():
                    binary2 += i
            return binary2



         def check_punctuation (letter):
        '''function that takes in a binary string and checks it in a excel dictionary of punctuation.
        Makes the length of the binary, if it is punctuation, equal to 8 by appending 2'''

        myfile = open('ascii_binary.csv','r')
        reader = csv.reader(myfile)

        x = ''
        nums_to_add = 8-len(letter)
        if nums_to_add == 1:
            binary += '2'
        if nums_to_add == 2:
            binary += '22'

        for row in reader:
            if letter == row[0]:
                return row[3]
        return None
    
    
  c. Once I have a list of binary, I iterate through pixels starting in the upper-left of the picture and going down each column before moving onto the next row. I strip out the last digit of each pixel and replace it with a bit from the binary list I just generated. Replacing the lowest order digit of the pixels does not noticeably change the picture, which is the point! I then pad the end of the message with eight 0s to signal message has ended.
  d. Handle edge cases that arise.
  
2. Decoding 
  a. Iterate through pixels, starting in the upper left (this is an arbitrary starting point. I start here because that's where the encoding starts), stripping off the last digits and ending when the last eight bits are all zero. 
  b. Convert binary list back into a message. Strip off the last eight zeros, iterate through list 8 bits at a time, check if punctuation and if so use custom dictionary. If not, convert to number and then convert to symbol. Output text message!
  
  
  
    for row in range(num_rows):
          for col in range(num_cols):
              r, g, b = image[row,col]
              binary_digits = strip_last_digit(r,g,b)
              bit_list.extend(binary_digits)

              '''if bit_list[-3] > 2:
                  bit_list = bit_list[0:-3]
              if bit_list[-2] > 2:
                  bit_list = bit_list[0:-2]
              if bit_list[-1] > 2:
                  bit_list = bit_list[0:-1]'''

              #print(r,g,b)
              #print(binary_digits)
              #print('bit list ',bit_list) 

              if bit_list[-8:-1] == [0,0,0,0,0,0,0]:
                  break
          break
      print('final bit list ', bit_list)
      return message_from_bits(bit_list)

    
    
  
Another fun project I did was to make a rudimentary green screen function which essentially replaces green background pixels that are part of the green screen and replaces them with corresponding pixels on the image I'm trying to superimpose. I first re-size the images to make sure they line up correctly.
