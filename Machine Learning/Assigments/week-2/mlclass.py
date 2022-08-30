import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from sklearn import metrics

def plot_decision_2d(clf,X,y,title="Decision Regions"):
    '''
    plot_decision_2d(clf,X,y)
    Plots a 2D decision region.
    '''
    # create a mesh to plot in
    x_min, x_max = X[:,0].min() - 1, X[:,0].max() + 1
    y_min, y_max = X[:,1].min() - 1, X[:,1].max() + 1

    h = (x_max-x_min)/1000.0 # step size in the mesh

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.3)

    # Plot also the training points
    plt.scatter(X[:,0], X[:,1], c=y, alpha=0.5, edgecolors='none')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.title(title)
    plt.grid(alpha=0.2)
    plt.show()

def simplemetrics(y_valid, y_score, scaler=1):
    figsize_a = 5.8*scaler
    figsize_b = 4.0*scaler
    fig = plt.figure(figsize=(figsize_a,figsize_b))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
    ax1 = fig.add_subplot(gs[0])

    fpr, tpr, _ = metrics.roc_curve(y_valid.ravel(), y_score.ravel())
    roc_auc = metrics.auc(fpr, tpr)

    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.08])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")

    ax2 = fig.add_subplot(gs[1])

    confmat = metrics.confusion_matrix(y_valid, y_score)

    ax2.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)
    ax2.xaxis.set_label_position('top')
    ax2.set_xlabel('Predicted')
    ax2.xaxis.set_label_position('top')
    ax2.set_ylabel('True')#, rotation=0)
    for i in range(confmat.shape[0]):
        for j in range(confmat.shape[1]):
            ax2.text(x=j, y=i, s=confmat[i, j], va='center', ha='center')
    plt.title('Confusion Matrix', y=1.5)
    plt.tick_params(
        axis='both',       # options x, y, both
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        left='off',
        right='off',
    ) # labels along the bottom edge are off

    ax2.text(-0.5, 3, u'Precision: %0.2f' % metrics.precision_score(y_valid, y_score), fontsize=12)
    ax2.text(-0.5, 3.5, u'Recall: %0.2f' % metrics.recall_score(y_valid, y_score), fontsize=12)
    ax2.text(-0.5, 4, u'F1 Score: %0.2f' % metrics.f1_score(y_valid, y_score), fontsize=12)
    plt.tight_layout()
    plt.show()
