git instructions:

   - name: Install Dependencies
   
      run: |
      
        python3 -m pip install --upgrade pip
        
        pip3 install -r requirements.txt
   
   - name: Run Tests
    
      run: |
      
        python3 -m pytest -v


steps to run application:

1) first run the rest services: python3 app.py
2) add the base url and host details to config (if changed)
3) run scheduler.py in seperate tab: python3 scheduler.py
