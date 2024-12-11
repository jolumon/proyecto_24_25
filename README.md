Proyecto del ciclo de grado superior de informática: Desarrollo de aplicaciones multiplataforma.

Se trata de un software de gestión de laboratorios cosméticos. Se podrá acceder a productos, materias primas, proveedores y clientes del laboratorio. En el módulo de productos se podrá acceder a la composición de los mismos, creación, eliminación y actualización de los productos. También se podrá lanzar la fabricación de un determinado producto y obtener la trazabilidad de las materias primas utilizadas en dicha fabricación. En el módulo de materias primas se podrá crear, eliminar, actualizar y dar de entrada en el laboratorio las materias primas necesarias para la producción de productos cosméticos. En el módulo de clientes se podrán crear, eliminar y actualizar los clientes. También se podrá ver los productos que tiene cada cliente. En el módulo de proveedores se podrá crear, eliminar, actualizar los proveedores. También se podrá ver las materias primas que cada proveedor suministra al laboratorio.



Para fabricar un cosmético se genera una orden de fabricación, indicando el cosmético y la cantidad a fabricar. Hay diferentes tipos de cosméticos. Los cosméticos están formados por materias primas en un determinado porcentaje. Cada cosmético es único( no pueden haber dos iguales con las mismas materias primas y porcentaje) y pertenece a un cliente. El cliente puede tener varios cosméticos. Las fabricaciones de cada cosmético quedan registradas en una orden de fabricación. La orden de fabricación debe registrar la trazabilidad de las materias primas utilizadas en función de la composición y la cantidad a fabricar, es decir, los lotes y cantidad de cada materia prima utilizada en la orden de fabricación para la fabricación del cosmético. Los cosméticos se fabrican en equipos según su capacidad y la cantidad a fabricar del cosmético. Estos equipos se encuentran en salas. En una sala pueden haber varios equipos. También se registran datos de los clientes y de los proveedores. Tablas maestro: clientes, proveedores, materias_primas, salas, equipos, ubicaciones, entradas, cosméticos, tipos, lotes_stock, ordenes_fabricacion. Tablas generadas por las relaciones: rel_cosmetico_materias_prima, rel_mps_proveedores, detalle_o_fabricacion. La fecha de caducidad se calcula automáticamente en función de la caducidad del cosmético que viene dada en años a partir de la fecha de fabricación. Se debe poder comprobar la existencia de materias primas necesarias para la fabricación. Si las materias primas son suficientes se procede a la confirmación de la orden de fabricación. La cantidad de materias primas empleadas se debe descontar de los lotes en stock de materias primas. Hay que tener en cuenta la cantidad de cada lote de materias primas. Puede que una orden necesite varios lotes de una misma materia prima para completar la cantidad necesaria para fabricar el cosmético.
Las materias primas entran en el laboratorio procedentes de un proveedor. Una materia prima pueden ser proporcionadas por varios proveedores y un proveedor puede suministrar varias materias primas. Se tienen que quedar registradas las entradas de materias primas con la fecha de entrada, lote de la materia prima, cantidad y la ubicación donde se guarda en la empresa. Cada lote de entrada de materia prima se almacena en una única ubicación. Una materia prima puede tener varios lotes que se encuentren en distintas ubicaciones.
Mediante el programa se podrán generar ordenes de fabricación para fabricar cosméticos. Comprobar la disponibilidad de las materias primas empleadas para la fabricación de un cosmético determinado. Conocer la trazabilidad de un cosmético mediante la orden de fabricación confirmada. Se podrá consultar el detalle de materias primas, clientes, proveedores, ubicaciones, equipos, salas, entradas de materias primas, cosméticos. Se podrán generar nuevas materias primas, clientes, proveedores, ubicaciones, equipos, salas, entradas de materias primas, cosméticos. También se podrán modificar y borrar las ya existentes.
