# CustomWidget
## Inicializar componente
Para inicializar este componente se hara con el siguiente constructor:  
AnimatedButton(width, height) donde width es anchura y height es altura del boton.  
El color de la animacion por defecto es en blanco y el texto del boton "boton".
## Funciones del componente
1. `getColor()`
  ```
  def getColor(self):
        return self._color
  ```
3. `setColor(color)`
  ```
  def setColor(self, color):
        self._color = color
        self.rec.setStyleSheet("background-color:"+color)
  ```
4. `getText()`
  ```
  def getText(self):
        return self._text
  ```
5. `setText(text)`
  ```
  def setText(self, text):
        self._text = text
        self.button.setText(text)
  ```
## Funcion de las funciones
Con `getColor()` nos devuelve un String donde te indica el color que tiene en el momento.  
Con `getText()` nos devuelve un String donde te indica el texto que tiene en el momento.  
Con `setColor(texto)` le pasamos un String con lo que queremos que ponga en el boton.  
Con `setText(texto)` le pasamos un String con lo que queremos que ponga en el boton.

##### [Pagina personal](https://fpintadoramos.github.io/)
