from django.db import models


# Create your models here.

class ResponseServer(models.Model):
    result = models.CharField(max_length=5000)
    score = models.DecimalField(decimal_places=2, max_digits=10)

    def get_data(self):
        res = {
            "result": self.result,
            "score": str(self.score)
        }
        return res


class ImageSearch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100)
    response = models.ManyToManyField('ResponseServer')

    def get_data(self):
        res = {
            "date": str(self.date),
            "client": self.client,
            "response": []
        }
        for response in self.response.all():
            res["response"].append(response.get_data())

        return res
