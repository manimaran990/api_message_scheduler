git instructins:

   - name: Install Dependencies
   
      run: |
      
        python3 -m pip install --upgrade pip
        
        pip3 install -r requirements.txt
   
   - name: Run Tests
    
      run: |
      
        python3 -m pytest -v
