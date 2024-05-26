import mysql.connector

class Request:
    def __init__(self):
        try:
            self.host = 'localhost'
            self.user = 'root'
            self.password = '0706042004'
            self.db = 'mydb'

            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.db)

            self.cursor = self.connection.cursor(dictionary=True)
            print("Successful connection to request")
        except mysql.connector.Error as err:
            print("Failed to connect to request:", err)

    def get_all_request(self):
        try:
            self.cursor.execute("select * from request")
            request = self.cursor.fetchall()

            if self.cursor.rowcount == 0:
                return {"message": "No request", "error": "Not Found", "status_code": 404}

            return request
        except mysql.connector.Error as err:
            return {'message': 'Failed to get all request', 'error': str(err), 'status_code': 500}

    def get_request_by_id(self, request_id):
        try:
            request_id = int(request_id)
            self.cursor.execute("select * from request where `request.id` = %s", (request_id,))
            request = self.cursor.fetchone()

            if self.cursor.rowcount == 0:
                return {"message": f"No request with id {request_id}", "error": "Not Found", "status_code": 404}

            return request
        except mysql.connector.Error as err:
            return {'message': 'Failed to get request', 'error': str(err), 'status_code': 500}
        except ValueError:
            return {"message": "Invalid request id", "error": "Bad Request", "status_code": 400}

    def add_request(self, url_params):
        try:
            self.cursor.execute('start transaction')
            self.cursor.execute(f"insert into request (`Request.id`, `Request.type`, `Request.message`,"
                                f"`User_User.id`, `Access_Access.id`)"
                                f"values {tuple([i for i in url_params.values()])}")
            self.connection.commit()

            if self.cursor.rowcount > 0:
                return {"message": "request added to requeste", "status_code": 200}
            else:
                return {"message": "request was not added to request", "error": "Not Acceptable", "status_code": 406}
        except mysql.connector.Error as err:
            self.connection.rollback()
            return {'message': 'Failed to add request', 'error': str(err), 'status_code': 500}

    def delete_request(self, request_id):
        try:
            request_id = int(request_id)
            self.cursor.execute('start transaction')
            rows_deleted = 0
            self.cursor.execute("delete from request where `request.id` = %s", (request_id,))
            rows_deleted += self.cursor.rowcount
            self.connection.commit()
            if rows_deleted > 0:
                return {"message": f"request {request_id} deleted from request", "status_code": 204}
            else:
                return {"message": f"request {request_id} was not deleted from request",
                        "error": "Not Found", "status_code": 404}
        except mysql.connector.Error as err:
            self.connection.rollback()
            return {'message': 'Failed to delete request', 'error': str(err), 'status_code': 500}
        except ValueError:
            return {"message": "Invalid request id", "error": "Bad Request", "status_code": 400}

    def edit_request(self, request_id, url_params):
        try:
            request_id = int(request_id)
            self.cursor.execute('start transaction')
            update_rows = 0
            for i in url_params.items():
                self.cursor.execute(f"update request set `{i[0]}` = '{i[1]}' where `request.id` = {request_id}")
                update_rows += 1
            self.connection.commit()

            if update_rows > 0:
                return {"message": f"request {request_id} updated in request", "status_code": 200}
            else:
                return {"message": f"request {request_id} was not updated in request",
                        "error": "Not Acceptable", "status_code": 406}
        except mysql.connector.Error as err:
            self.connection.rollback()
            return {'message': 'Failed to update request', 'error': str(err), 'status_code': 500}
        except ValueError:
            return {"message": "Invalid request id", "error": "Bad Request", "status_code": 400}